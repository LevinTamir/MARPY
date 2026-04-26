"""Launch MARPY on real hardware.

Assumes the micro-ROS agent is already running:
  docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888 -v6

The ESP32 firmware handles /cmd_vel, /joint_states, and /imu directly.
This launch file starts:
  - robot_state_publisher (URDF TFs)
  - odometry_node (computes /odom + odom->base_footprint TF from /joint_states)
  - rviz2 (visualization, using the same config as the sim launch)

Teleop is launched separately from another terminal:
  ros2 run teleop_twist_keyboard teleop_twist_keyboard
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_dir = get_package_share_directory("marpy_description")

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(pkg_dir, "urdf", "marpy.xacro"),
        description="Absolute path to robot xacro file",
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]),
        value_type=str,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )

    odometry_node = Node(
        package="marpy_localization",
        executable="odometry_node",
        name="odometry_node",
        output="screen",
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(pkg_dir, "rviz", "display.rviz")],
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        odometry_node,
        rviz,
    ])
