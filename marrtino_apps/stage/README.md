# Using stage simulator for MARRtino

## Install

Note: installation is not necessary when using dockerized components.

* Using ROS package `stage_environments`

    https://bitbucket.org/iocchi/stage_environments.git


## Run

Launch simulator and map server


    roslaunch simrobot.launch


Arguments

    <arg name="world_file" default="world.world" />
    <arg name="base_frame" default="base_frame" />
    <arg name="laser_topic" default="scan" />
    <arg name="laser_frame" default="laser_frame" />
    <arg name="worldsdir" default="$(env MARRTINO_APPS_HOME)/stage/worlds" />
    <arg name="stageros_args" default="" />   <!-- use "-g" to launch stage without GUI -->

    <arg name="use_mapserver" default="true" />
    <arg name="mapsdir" default="$(env MARRTINO_APPS_HOME)/mapping/maps" />
    <arg name="map_name" default="map" />


Topics services and frames used by the simulator


    Node [/stageros]

    Publications: 
     * /rosout [rosgraph_msgs/Log]
     * /tf [tf2_msgs/TFMessage]
     * /clock [rosgraph_msgs/Clock]
     * /odom [nav_msgs/Odometry]
     * /base_pose_ground_truth [nav_msgs/Odometry]
     * /scan [sensor_msgs/LaserScan]

    Subscriptions: 
     * /stageGUIRequest [unknown type]
     * /clock [rosgraph_msgs/Clock]
     * /cmd_vel [unknown type]

    Services: 
     * /stageros/set_logger_level
     * /stageros/get_loggers

    Frames:
    - base_footprint_frame 
    - base_frame
    - laser_frame


## Test

Use teleop app to drive the robot in the environment.



