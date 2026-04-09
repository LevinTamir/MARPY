import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_dir = get_package_share_directory("merpy_description")

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(pkg_dir, "urdf", "merpy.xacro"),
        description="Absolute path to robot xacro file",
    )

    world_name_arg = DeclareLaunchArgument(
        name="world_name",
        default_value="empty",
        description="Gazebo world file name (without .sdf extension)",
    )

    world_path = PathJoinSubstitution([
        pkg_dir,
        "worlds",
        PythonExpression(
            ["'", LaunchConfiguration("world_name"), "' + '.sdf'"]
        ),
    ])

    model_path = os.path.dirname(pkg_dir)
    gazebo_resource_path = SetEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        model_path,
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]),
        value_type=str,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py"
            ),
        ]),
        launch_arguments={"gz_args": PythonExpression(["'", world_path, " -v 4 -r'"])}.items(),
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic", "robot_description",
            "-name", "merpy",
            "-x", "0.0",
            "-y", "0.0",
            "-z", "0.05",
        ],
    )

    gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
            "/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model",
            "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
        ],
        output="screen",
    )

    return LaunchDescription([
        model_arg,
        world_name_arg,
        gazebo_resource_path,
        robot_state_publisher,
        gazebo,
        spawn_entity,
        gz_bridge,
    ])
