"""Compute differential-drive odometry from wheel joint states.

Subscribes to /joint_states (published by ESP32 or Gazebo) and produces:
  - /odom  (nav_msgs/Odometry)
  - /odom_path  (nav_msgs/Path) — accumulated route the robot has traveled
  - odom -> base_footprint TF broadcast

This node is used in both simulation and real hardware so the data
pipeline is identical.
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import (
    PoseStamped,
    TransformStamped,
    Quaternion,
)
from tf2_ros import TransformBroadcaster


def yaw_to_quaternion(yaw: float) -> Quaternion:
    """Convert a yaw angle (radians) to a Quaternion message."""
    q = Quaternion()
    q.z = math.sin(yaw / 2.0)
    q.w = math.cos(yaw / 2.0)
    return q


class OdometryNode(Node):
    # Robot geometry (must match URDF and firmware)
    WHEEL_RADIUS = 0.033      # metres
    WHEEL_SEPARATION = 0.116  # metres (2 * 0.058)

    def __init__(self):
        super().__init__("odometry_node")

        # State
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.prev_left_pos = None
        self.prev_right_pos = None
        self.prev_time = None

        # Path accumulator
        self.path = Path()
        self.path.header.frame_id = "odom"

        # Publishers
        self.odom_pub = self.create_publisher(Odometry, "/odom", 10)
        self.path_pub = self.create_publisher(Path, "/odom_path", 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscriber
        self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_states_cb,
            QoSProfile(depth=10),
        )

        self.get_logger().info("Odometry node started")

    def joint_states_cb(self, msg: JointState):
        # Find left and right wheel indices
        try:
            left_idx = list(msg.name).index("left_wheel_joint")
            right_idx = list(msg.name).index("right_wheel_joint")
        except ValueError:
            return

        left_pos = msg.position[left_idx]
        right_pos = msg.position[right_idx]
        now = self.get_clock().now()

        # Skip first message (need a previous reading to compute deltas)
        if self.prev_left_pos is None:
            self.prev_left_pos = left_pos
            self.prev_right_pos = right_pos
            self.prev_time = now
            return

        # Compute deltas
        dl = (left_pos - self.prev_left_pos) * self.WHEEL_RADIUS
        dr = (right_pos - self.prev_right_pos) * self.WHEEL_RADIUS
        dt_sec = (now - self.prev_time).nanoseconds * 1e-9

        self.prev_left_pos = left_pos
        self.prev_right_pos = right_pos
        self.prev_time = now

        if dt_sec <= 0.0:
            return

        # Differential drive kinematics
        ds = (dr + dl) / 2.0
        dtheta = (dr - dl) / self.WHEEL_SEPARATION

        self.x += ds * math.cos(self.theta + dtheta / 2.0)
        self.y += ds * math.sin(self.theta + dtheta / 2.0)
        self.theta += dtheta

        # Velocities
        v = ds / dt_sec
        omega = dtheta / dt_sec

        # Publish odometry message
        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_footprint"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation = yaw_to_quaternion(self.theta)

        odom.twist.twist.linear.x = v
        odom.twist.twist.angular.z = omega

        self.odom_pub.publish(odom)

        # Append to path and publish
        pose_stamped = PoseStamped()
        pose_stamped.header.stamp = now.to_msg()
        pose_stamped.header.frame_id = "odom"
        pose_stamped.pose = odom.pose.pose
        self.path.poses.append(pose_stamped)
        self.path.header.stamp = now.to_msg()
        self.path_pub.publish(self.path)

        # Broadcast odom -> base_footprint transform
        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_footprint"
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation = yaw_to_quaternion(self.theta)

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
