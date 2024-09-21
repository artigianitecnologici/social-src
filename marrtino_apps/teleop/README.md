# Teleop

## Install

Note: installation is not necessary when using dockerized components.


Download the following packages in your catkin workspace and compile them with catkin_make:


    https://github.com/Imperoli/gradient_based_navigation


For joystick control, you also need the ROS node joy.


    sudo apt install ros-kinetic-joy


For obstacle avoidance, you also need a laser device (see [laser](https://bitbucket.org/iocchi/marrtino_apps/src/master/laser/) section)


## Run

* Joystick/keyboard control

        cd teleop
        roslaunch teleop.launch [use_joystick:=false]

    Option ```use_joystick:=false``` to use keyboard instead of joystick


* Joystick/keyboard control with obstacle avoidance

        cd navigation
        roslaunch obstacle_avoidance.launch

        cd teleop
        roslaunch teleop.launch cmd_vel:=joystick_cmd_vel [use_joystick:=false]


* Visualizing sensor data

    If you want to display from a remote PC

        export ROS_MASTER_URI=http://<ROBOT_IP>:11311/

    Run the rviz visualizer

        cd navigation
        rosrun rviz rviz -d nav.rviz

    If not running with a localizer or a mapper, change the main frame from ```map``` to ```odom```.

