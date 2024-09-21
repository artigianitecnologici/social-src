# Robot #


## Install ##

Note: installation is not necessary when using dockerized components.

Download the following packages in your catkin workspace and compile them with catkin_make:

* https://gitlab.com/srrg-software/srrg_cmake_modules
* https://gitlab.com/srrg-software/srrg_core
* https://gitlab.com/srrg-software/srrg_core_ros
* https://gitlab.com/srrg-software/srrg2_orazio_core
* https://gitlab.com/srrg-software/srrg2_orazio_ros

## Run ##

```
roslaunch robot.launch
```

* Subscribers
```
cmd_vel - geometry_msgs/Twist
```

* Publishers
```
odom - nav_msgs.msg/Odometry
```

* Tf
```
odom -> base_frame
```




