#!/usr/bin/env bash
set -e

source "/opt/ros/$ROS_DISTRO/setup.bash"

# Source workspace if built
if [ -f "/home/robot/ws/install/setup.bash" ]; then
    source "/home/robot/ws/install/setup.bash"
fi

exec "$@"
