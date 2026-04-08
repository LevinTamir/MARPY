# ROS2 Setup Guide

Complete setup guide for running MERPY on Ubuntu 24.04 with ROS2 Jazzy.

## Option A: Docker (Recommended for Beginners)

Docker is the easiest way to get started - no ROS2 installation needed on your host machine.

### Prerequisites
- [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the Workspace

```bash
git clone https://github.com/LevinTamir/MERPY.git merpy_ws
cd merpy_ws
```

### 2. Start the Containers

This launches both the **micro-ROS agent** and the **ROS2 workspace** container:

```bash
cd docker
docker compose up -d
```

### 3. Enter the Workspace

```bash
docker exec -it merpy_ws bash
```

### 4. Build the Workspace

Inside the container:
```bash
colcon build --symlink-install
source install/setup.bash
```

### 5. Run Teleop

```bash
ros2 run teleop_control_node teleop_control
```

Now drive your robot with `i`, `j`, `k`, `l` keys!

---

## Option B: Native Installation

> This section assumes you already have **ROS2 Jazzy installed** on Ubuntu 24.04.
> If not, follow the [official installation guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) first.

### 1. Clone and Build the Workspace

```bash
git clone https://github.com/LevinTamir/MERPY.git merpy_ws
cd merpy_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

### 2. Run the micro-ROS Agent

The agent bridges the ESP32 (UDP over WiFi) to the ROS2 network.

**Using Docker (easiest):**
```bash
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888 -v6
```

**Or install natively:**
```bash
sudo apt install ros-jazzy-micro-ros-agent
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
```

### 3. Verify the Connection

Once the ESP32 is powered on and connected to WiFi, you should see it connect in the agent output. Then verify:

```bash
# List active topics
ros2 topic list
# Expected: /cmd_vel, /joint_states

# Check encoder data from ESP32
ros2 topic echo /joint_states

# Send a test velocity command
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}, angular: {z: 0.0}}" --once
```

### 4. Run Teleop

```bash
ros2 run teleop_control_node teleop_control
```

## Network Configuration

| Setting | Value |
|---------|-------|
| ESP32 WiFi | Must be same network as PC |
| Agent Port | 8888 (UDP) |
| ROS Domain ID | 0 (default) |
| Firewall | Allow UDP port 8888: `sudo ufw allow 8888/udp` |

## Quick Reference

```bash
# Terminal 1: micro-ROS agent
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888 -v6

# Terminal 2: Teleop
cd merpy_ws
source install/setup.bash
ros2 run teleop_control_node teleop_control
```
