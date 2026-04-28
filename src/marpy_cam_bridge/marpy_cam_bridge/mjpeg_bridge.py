"""Pull MJPEG frames from the ESP32-CAM and republish as sensor_msgs/Image.

The cam firmware serves a multipart/x-mixed-replace stream at
http://marpy-cam.local/stream. cv2.VideoCapture handles the multipart parsing
and JPEG decoding for us; we just convert each frame to a ROS image message
and publish.
"""

import threading
import time

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class MjpegBridge(Node):
    def __init__(self):
        super().__init__("marpy_cam_bridge")

        self.declare_parameter("stream_url", "http://marpy-cam.local:81/stream")
        self.declare_parameter("topic", "/camera/image_raw")
        self.declare_parameter("frame_id", "camera_optical_frame")
        self.declare_parameter("reconnect_delay_s", 2.0)

        self._stream_url = self.get_parameter("stream_url").value
        self._frame_id = self.get_parameter("frame_id").value
        self._reconnect_delay = float(self.get_parameter("reconnect_delay_s").value)

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
            cap = cv2.VideoCapture(self._stream_url)
            if not cap.isOpened():
                self.get_logger().warn(
                    f"cannot open {self._stream_url}; retrying in {self._reconnect_delay:.1f}s"
                )
                cap.release()
                if self._stop.wait(self._reconnect_delay):
                    return
                continue

            self.get_logger().info("stream open")
            try:
                while not self._stop.is_set() and rclpy.ok():
                    ok, frame = cap.read()
                    if not ok or frame is None:
                        self.get_logger().warn("stream read failed; reconnecting")
                        break
                    self._publish(frame)
            finally:
                cap.release()

            if self._stop.wait(self._reconnect_delay):
                return

    def _publish(self, frame):
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
