# picar-x
ROS Node for the Sunfounder PiCarX.

## Background
This software was originally developed for the Queen's ELEC390 Course.
The reasoning for developing this software was to fix several issues found in the Python code present on the Sunfounder website.

Additionally, this project has the added benifit of being compatible with ROS 2 Humble for easy prototyping and rapid development.

# Getting Started
## Prerequisites
This code must be run on the Raspberry Pi.
It can be tested on other devices by defining the `TEST` flag in `pix_driver.hpp`.
Additionally, dependencies must be installed prior to running the code.

Dependencies:
 - Ubuntu 22.04
 - ROS 2 Humble
 - ClangD
 - GpioD (Usually present on Raspberry Pi by default)
 
 Optional:
 - `camera_ros` Camera Node
 - ZSH (for using build script)


 *DO NOT use the Sunfounder provided Raspberry Pi image - Use Ubuntu 22.04 instead.*


 ## Usage
 To use this control module, first setup a ROS workspace.
 Then, clone this repository into the `src/` folder.
 Optionally, the `build.sh` and launch files can be moved to the `ros_ws` base folder, or deleted.

 After installed, the code can be built as described in the ROS Getting Started Tutorials.

 ## Modifications/Parameters
 Several parameters are present in this code that can be modified.

 ### Turn Offset
 The `turn offset` controls the offset used when turning.
 This value can be modified to help the car drive in a straight line.
 This value can be changed in the launch file `launch/launch_picar.py`, or in the C++ file `src/node.cpp`.

 ### Diff Ratio
 The Diff Ratio controls the ratio used for software differential turning.
 This is a feature not present within the default Sunfounder code.
 Setting the `diff_ratio` parameter to `0` disables it.
 The `diff_ratio` parameter can be changed in the launch file `launch/launch_picar.py`, or in the C++ file `src/node.cpp`.

### PWM/Servos
A major issue in the original Sunfounder code was incorrect constants being used for the servo control.
Within the `include/pix_driver.hpp` file are several variables following the format `_(min+max)_pwm`.
These variables can be tuned to adjust the maximum and minimum ranges of servos to give more linear control of the servo angles.
Without proper tuning, the degree value applied to the servo will not match the actual angle of the servo.

The values currently present were tuned based off of a single car in 2025.
It is highly likely that these will need to be adjusted.

### Camera Positioning
The camera servos use an additional tuning parameter `cam_off_deg` present in the `include/pix_driver.hpp` file.
In testing, it was found that the camera servos were both off center by the same amount.
This parameter was integrated into the code to solve this issue.

This parameter may be a result of physical limitations of the car, or of incorrect assembly.
The exact cause of needing this value was never explored.


# Sample Usage
For a sample project that uses this code, see my groups [ELEC390 Code](https://github.com/hendrixgg/ELEC390/tree/main) posted on GitHub.

Specifically, the `ros_ws` folder contains the `pix_driver` node, containing the code from this repo, and the `driver` node, containing an example of possible usage.


Furthermore, the PiCarX uses a servo for steering.
This can result in jerky movement.
For an example of how to fix this issue, see the following code snippet, shown below.
```cpp
float exponential(float joystickVal, float driveExp, float joydead, float motorMin, float motorMax){
  float joySign;
  float joyMax = motorMax - joydead;
  float joyLive = fabs(joystickVal) - joydead;
  if(joystickVal > 0){joySign = 1;}
  else if(joystickVal < 0){joySign = -1;}
  else{joySign = 0;}
  int power = joySign * (motorMin + ((motorMax - motorMin) * (powf(joyLive, driveExp) / powf(joyMax, driveExp))));
  return power;
}

void Driver::line_dev_callback(const std_msgs::msg::Float32::SharedPtr msg){
    error = -(msg->data - 42);
    float derr = (error - error_last);
    error_sum = (error + error_sum)/2;
    error_last = error;
    float p = this->param_pid_p*error;
    float i = this->param_pid_i*error_sum;
    float d = this->param_pid_d*derr;
    float pow = p + i + d;
    float exp = pow;//exponential(pow, 1.2, 2, 0, 30);
    if(exp >= 30) exp = 30;
    if(exp <= -30) exp = -30;
    this->turn_angle = exp*this->param_turn_factor + this->turn_angle*(1-this->param_turn_factor);
    this->drive_pow = this->param_drive_power;
}
```

A full explanation of the project can also be found at [https://jchisholm204.github.io/posts/elec390/#driving-state](https://jchisholm204.github.io/posts/elec390/)

# Licencing and Credit
This code can be used and modified in any way so long as credit is given to the original author, Jacob Chisholm.
