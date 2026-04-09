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
        rviz,
    ])
