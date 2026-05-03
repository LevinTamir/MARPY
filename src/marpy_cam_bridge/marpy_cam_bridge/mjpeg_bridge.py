"""Pull MJPEG frames from the ESP32-CAM and republish as sensor_msgs/Image.

The cam serves a multipart/x-mixed-replace stream at
http://marpy-cam.local:81/stream. We open it with `requests` (one long-lived
HTTP connection), parse the multipart envelope by hand, and decode each JPEG
part with cv2.imdecode.

Why not cv2.VideoCapture: OpenCV's videoio backends (FFmpeg/GStreamer) are
unreliable on multipart/x-mixed-replace, and when they fail they leave the
TCP socket lingering. The cam's httpd has only a handful of worker slots, so
a few failed retries wedge it for every other client (including a browser).
A plain requests.get(stream=True) gives us deterministic socket teardown via
the context manager.
"""

import threading
import time
from typing import Optional

import cv2
import numpy as np
import rclpy
import requests
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


# Read in chunks small enough to keep latency low but large enough to avoid
# syscall overhead. JPEG frames at QVGA are typically 5-20 kB.
_READ_CHUNK = 4096


class StreamError(Exception):
    """Raised when the multipart stream is malformed or the peer drops."""


def _parse_boundary(content_type: str) -> str:
    # "multipart/x-mixed-replace;boundary=foo" or with quotes/spaces.
    for part in content_type.split(";"):
        part = part.strip()
        if part.lower().startswith("boundary="):
            return part.split("=", 1)[1].strip().strip('"')
    raise StreamError(f"no boundary in Content-Type: {content_type!r}")


def _read_exact(it, buf: bytearray, n: int) -> None:
    """Pull bytes from `it` into `buf` until len(buf) >= n."""
    while len(buf) < n:
        try:
            chunk = next(it)
        except StopIteration:
            raise StreamError("connection closed mid-frame")
        if chunk:
            buf.extend(chunk)


def _read_until(it, buf: bytearray, sep: bytes, start: int = 0) -> int:
    """Pull bytes until `sep` appears in buf at or after `start`. Return its index."""
    while True:
        idx = buf.find(sep, start)
        if idx >= 0:
            return idx
        try:
            chunk = next(it)
        except StopIteration:
            raise StreamError("connection closed scanning for separator")
        if chunk:
            # Only need to rescan from near the previous tail.
            start = max(start, len(buf) - len(sep) + 1)
            buf.extend(chunk)


class MjpegBridge(Node):
    def __init__(self):
        super().__init__("marpy_cam_bridge")

        self.declare_parameter("stream_url", "http://marpy-cam.local:81/stream")
        self.declare_parameter("topic", "/camera/image_raw")
        self.declare_parameter("frame_id", "camera_optical_frame")
        self.declare_parameter("reconnect_delay_s", 2.0)
        # Connect timeout is also generous: when the cam's httpd backlog
        # is full (e.g. recovering from a previous failed client), new SYNs
        # may be silently dropped for a few seconds.
        self.declare_parameter("connect_timeout_s", 10.0)
        # Generous read timeout: the cam's wifi link can stall for several
        # seconds at a time, and its single httpd worker can take ~send_wait_timeout
        # to free after a previous client disconnects. Too tight a timeout
        # turns a recoverable hiccup into a reconnect storm.
        self.declare_parameter("read_timeout_s", 15.0)
        # 0=none, 90=CCW, 180=180, 270=CW. The cam is mounted rotated on the
        # robot, so we straighten it here before publishing.
        self.declare_parameter("rotate_deg", 90)

        self._stream_url = self.get_parameter("stream_url").value
        self._frame_id = self.get_parameter("frame_id").value
        self._reconnect_delay = float(self.get_parameter("reconnect_delay_s").value)
        self._connect_timeout = float(self.get_parameter("connect_timeout_s").value)
        self._read_timeout = float(self.get_parameter("read_timeout_s").value)
        self._rotate_deg = int(self.get_parameter("rotate_deg").value)

        topic = self.get_parameter("topic").value
        self._pub = self.create_publisher(Image, topic, 10)
        self._bridge = CvBridge()

        self.get_logger().info(f"streaming {self._stream_url} -> {topic}")

        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def shutdown(self):
        self._stop.set()
        self._thread.join(timeout=2.0)

    def _run(self):
        while not self._stop.is_set() and rclpy.ok():
            try:
                self._stream_once()
            except (requests.RequestException, StreamError, OSError) as e:
                self.get_logger().warn(
                    f"stream error ({type(e).__name__}: {e}); "
                    f"reconnecting in {self._reconnect_delay:.1f}s"
                )
            if self._stop.wait(self._reconnect_delay):
                return

    def _stream_once(self):
        # Connection: close keeps the cam's socket pool from being held by a
        # half-closed keep-alive when we tear down. stream=True streams the
        # response body without buffering it whole into memory.
        headers = {"Connection": "close", "Accept": "*/*"}
        r = requests.get(
            self._stream_url,
            stream=True,
            timeout=(self._connect_timeout, self._read_timeout),
            headers=headers,
        )
        try:
            r.raise_for_status()
            self._consume_stream(r)
        finally:
            # requests.Response.__exit__ tries to drain the body before close,
            # which on a broken chunked stream can hang or throw silently and
            # leak the socket. Force-close the underlying urllib3 connection
            # so the cam frees its httpd worker slot immediately.
            try:
                r.raw.close()
            except Exception:
                pass
            try:
                r.close()
            except Exception:
                pass

    def _consume_stream(self, r):
        ctype = r.headers.get("Content-Type", "")
        if "multipart/" not in ctype.lower():
            raise StreamError(f"unexpected Content-Type: {ctype!r}")
        boundary = _parse_boundary(ctype)
        self.get_logger().info(f"stream open (boundary={boundary!r})")

        # The wire format is, repeated per frame:
        #     \r\n--<boundary>\r\n
        #     Content-Type: image/jpeg\r\n
        #     Content-Length: <N>\r\n
        #     [optional headers]\r\n
        #     \r\n
        #     <N JPEG bytes>
        sep = b"--" + boundary.encode("ascii")
        it = r.iter_content(chunk_size=_READ_CHUNK)
        buf = bytearray()

        # Skip the preamble (anything before the first boundary).
        idx = _read_until(it, buf, sep)
        del buf[: idx + len(sep)]

        frames = 0
        last_log = time.monotonic()
        while not self._stop.is_set() and rclpy.ok():
            self._consume_line_ending(it, buf)
            if buf.startswith(b"--"):
                # End-of-stream marker (--boundary--). The cam doesn't send
                # this, but be polite about it.
                return
            hdr_end = _read_until(it, buf, b"\r\n\r\n")
            hdrs = bytes(buf[:hdr_end]).decode("latin-1", errors="replace")
            del buf[: hdr_end + 4]

            clen = self._parse_content_length(hdrs)
            if clen is None or clen <= 0 or clen > 4 * 1024 * 1024:
                raise StreamError(f"bad/missing Content-Length in {hdrs!r}")

            _read_exact(it, buf, clen)
            jpeg = bytes(buf[:clen])
            del buf[:clen]

            frame = cv2.imdecode(
                np.frombuffer(jpeg, dtype=np.uint8), cv2.IMREAD_COLOR
            )
            if frame is None:
                self.get_logger().warn(
                    f"jpeg decode failed ({clen} bytes); skipping"
                )
            else:
                self._publish(frame)
                frames += 1

            now = time.monotonic()
            if now - last_log >= 5.0:
                fps = frames / (now - last_log)
                self.get_logger().info(f"published {frames} frames ({fps:.1f} fps)")
                frames = 0
                last_log = now

            # The next boundary follows. Walk to it.
            idx = _read_until(it, buf, sep)
            del buf[: idx + len(sep)]

    @staticmethod
    def _consume_line_ending(it, buf: bytearray) -> None:
        # The cam emits "\r\n" right after the boundary token; tolerate "\n".
        _read_exact(it, buf, 1)
        if buf[:1] == b"\r":
            _read_exact(it, buf, 2)
            del buf[:2]
        elif buf[:1] == b"\n":
            del buf[:1]

    @staticmethod
    def _parse_content_length(hdrs: str) -> Optional[int]:
        for line in hdrs.split("\r\n"):
            if line.lower().startswith("content-length:"):
                try:
                    return int(line.split(":", 1)[1].strip())
                except ValueError:
                    return None
        return None

    _ROT_CODES = {
        90: cv2.ROTATE_90_COUNTERCLOCKWISE,
        180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_CLOCKWISE,
    }

    def _publish(self, frame):
        rot = self._ROT_CODES.get(self._rotate_deg)
        if rot is not None:
            frame = cv2.rotate(frame, rot)
        msg = self._bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self._frame_id
        self._pub.publish(msg)


def main():
    rclpy.init()
    node = MjpegBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
