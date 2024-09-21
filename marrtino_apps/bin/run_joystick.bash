#!/bin/bash

# Start robot and joystick nodes

cd $HOME/src/marrtino_apps/teleop
roslaunch robot_teleop.launch use_joystick:=true

