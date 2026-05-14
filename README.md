# ROS 2 Speed Controller

A fundamental ROS 2 project built with **ROS 2 Jazzy** demonstrating how to create custom services, use parameters, and publish velocity commands (`cmd_vel`) to control a mobile robot.

## Features
- **Custom ROS 2 Interfaces**: Includes a custom `SetSpeed` service.
- **Speed Service Node**: A Python-based node that securely sets linear and angular velocities.
- **Parameter Validation**: Utilizes ROS 2 parameters to limit maximum allowable speeds for safety.

## Packages
- `my_robot`: Contains the core logic, including the `speed_service` Python node.
- `my_robot_interfaces`: Contains the custom C++ service definitions (`SetSpeed.srv`).

## Prerequisites
- Ubuntu 24.04 (Noble Numbat)
- [ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html)
- Python 3.12 (System default)

## Installation & Build

1. Clone the repository into your workspace's `src` directory:
   ```bash
   mkdir -p ~/robot_ws/src
   cd ~/robot_ws/src
   git clone <YOUR-GITHUB-REPO-URL> .
   ```

2. Build the workspace (make sure Conda is deactivated if you use it):
   ```bash
   cd ~/robot_ws
   colcon build
   ```

3. Source the environment:
   ```bash
   source install/setup.bash
   ```

## Usage

1. Run the Speed Service node:
   ```bash
   ros2 run my_robot speed_service
   ```

2. In another terminal, call the service to set the robot's speed:
   ```bash
   ros2 service call /set_speed my_robot_interfaces/srv/SetSpeed "{linear_speed: 0.5, angular_speed: 1.0}"
   ```
   *Note: Requests exceeding the `max_linear_speed` parameter will be safely rejected.*
