# Simulation

Run MARPY in Gazebo Ignition without any hardware. The simulation uses the same `/cmd_vel` and `/joint_states` topics as the real robot, so teleop and odometry work identically.

## Prerequisites

Install the following ROS2 Jazzy packages (Ubuntu 24.04):

```bash
sudo apt update
sudo apt install -y \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-xacro \
  ros-jazzy-rviz2 \
  ros-jazzy-teleop-twist-keyboard
```

Build the workspace:

```bash
cd ~/marpy_ws
colcon build --symlink-install
source install/setup.bash
```

## Launch the Simulation

The `sim.launch.py` file starts Gazebo, RViz, and the odometry node in one command:

```bash
ros2 launch marpy_bringup sim.launch.py
```

This launches:
- **Gazebo Ignition** with the MARPY robot spawned in an empty world
- **RViz** for visualization (TF, robot model, odometry path)
- **Odometry node** computing wheel odometry from `/joint_states`

## Drive the Robot

In a separate terminal:

```bash
source ~/marpy_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Use the keyboard to drive. You should see:
- The robot moving in Gazebo
- The odometry path (`/odom_path`) drawing in RViz
- The TF tree updating in real time

## Visualize the Odometry Path in RViz

If the path is not already visible in RViz:

1. Click **Add** in the Displays panel
2. Select **By topic** → `/odom_path` → **Path**
3. Click **OK**

The path will draw the route the robot has traveled in the odom frame.

## View the URDF Model Only

To inspect the robot model in RViz without Gazebo:

```bash
ros2 launch marpy_description display.launch.py
```

## Custom Worlds

Pass a custom world file:

```bash
ros2 launch marpy_bringup sim.launch.py world_name:=my_world
```

World files are located in `src/marpy_description/worlds/` (SDF format).

## Troubleshooting

**Gazebo doesn't start or hangs:**
```bash
pkill -9 -f "gz sim|rviz2|robot_state_publisher|parameter_bridge"
```
Then relaunch.

**Robot doesn't move with teleop:**
- Make sure the teleop terminal is focused (it reads keypresses)
- Check that the Gazebo bridge is running: `ros2 topic list` should show `/cmd_vel`

**No odometry path in RViz:**
- Verify the odometry node is running: `ros2 node list` should show `/odometry_node`
- Check the topic: `ros2 topic echo /odom_path --once`
