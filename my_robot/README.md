# ROS 2 & Mobile Robot Simulation with Gazebo

A fundamental ROS 2 project built with **ROS 2 Jazzy** demonstrating how to create custom services, actions, use parameters, and publish velocity commands (`cmd_vel`) to control a mobile robot in Gazebo.

## 🧠 Core ROS 2 Concepts Demonstrated

This project is built as a learning resource to demonstrate the five foundational concepts of ROS 2:

1. **Nodes**:
   - `speed_service`: A node that acts as a server to regulate robot speed.
   - `drive_action_server`: A node that handles long-running tasks (driving a specific distance) while providing live feedback.
   - `teleop_keyboard`: A node that captures keyboard inputs to control the robot interactively.
2. **Topics**:
   - **Publisher**: The `teleop_keyboard`, `speed_service`, and `drive_action_server` nodes publish `geometry_msgs/msg/Twist` messages to the `/cmd_vel` topic to move the robot's wheels.
   - **Subscriber**: The `drive_action_server` subscribes to the `/odom` topic to calculate the distance traveled based on wheel odometry.
3. **Services**:
   - The project features a custom service `SetSpeed` (defined in `my_robot_interfaces`). The `speed_service` node acts as a Service Server that receives a request (linear/angular speed), processes it, and returns a success/failure response instantly.
4. **Actions**:
   - The `DriveDistance` action allows the robot to drive a specific distance. Unlike services, actions are for long-running, preemptable tasks. The `drive_action_server` processes the goal, sends live **feedback** (percentage completed), and returns a final **result** once the robot reaches the target.
5. **Parameters**:
   - The `speed_service` node uses a parameter `max_linear_speed` to validate safety limits dynamically. If a user requests a speed higher than this parameter, the service rejects it.

## 📦 Packages

- `my_robot`: Contains the core logic, including the nodes for teleop, service, and action server.
- `my_robot_interfaces`: Contains the custom C++ interface definitions (`SetSpeed.srv` and `DriveDistance.action`).

## ⚙️ Prerequisites

- Ubuntu 24.04 (Noble Numbat)
- [ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html)
- Python 3.12 (System default)

## 🛠️ Installation & Build

1. Clone the repository into your workspace's `src` directory:

   ```bash
   mkdir -p ~/robot_ws/src
   cd ~/robot_ws/src
   # Jangan lupa titik di akhir agar isinya langsung terekstrak ke src/
   git clone https://github.com/youngIcom/mobile-robot-simulation-ros2-gazebo.git .
   ```

2. Build the workspace (make sure Conda is deactivated if you use it):

   ```bash
   cd ~/robot_ws
   colcon build
   ```

3. Source the environment:
   ```bash
   source install/setup.zsh
   ```

## 🚀 Usage

_Always make sure to source your workspace (`source install/setup.zsh`) in every new terminal._

### 1. Launch the Gazebo Simulation

Start the simulation world and spawn the robot.

Run Robot 1 (Simple Robot using 2 wheels, free wheel, and imu sensor)

```bash
ros2 launch my_robot sim.launch.py
```
Run Robot 2 (Custom Design with 2 wheels, free wheel and IMU BNO055 Design)
This project was design by Onshape

```bash
ros2 launch my_robot assembly_sim.launch.py
```

### 2. Manual Control (Teleop Keyboard)

In a new terminal, run the teleop node to control the robot manually using your keyboard (`W`, `A`, `S`, `D`, `Space`).

```bash
ros2 run my_robot teleop_keyboard
```

### 3. Using the Speed Service

Start the speed service node in a new terminal:

```bash
ros2 run my_robot speed_service
```

In another terminal, call the service to set the robot's speed:

```bash
ros2 service call /set_speed my_robot_interfaces/srv/SetSpeed "{linear_speed: 0.5, angular_speed: 1.0}"
```

_Note: Requests exceeding the `max_linear_speed` parameter will be safely rejected by the node._

### 4. Using the Drive Action Server

Start the action server node:

```bash
ros2 run my_robot drive_action_server
```

Send an action goal to drive the robot 3.0 meters forward at 0.4 m/s, while tracking its live progress:

```bash
ros2 action send_goal -f /drive_distance my_robot_interfaces/action/DriveDistance "{distance: 3.0, speed: 0.4}"
```
