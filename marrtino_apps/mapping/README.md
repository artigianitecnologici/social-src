# Navigation #


## Install ##

Note: installation is not necessary when using dockerized components.

* [gmapping](http://wiki.ros.org/gmapping)


    sudo apt-get install ros-kinetic-gmapping


## Run ##

1. Run robot with laser 

    See  [robot](https://bitbucket.org/iocchi/marrtino_apps/src/master/robot/) and [laser](https://bitbucket.org/iocchi/marrtino_apps/src/master/laser) sections 

2. Run mapper

        roslaunch gmapping.launch


3. Drive the robot around the environment

    For example, you can use [teleop](https://bitbucket.org/iocchi/marrtino_apps/src/master/teleop/)


4. See the map while building

    If you want to display from a remote PC

        export ROS_MASTER_URI=http://<ROBOT_IP>:11311/


    Run rviz visualizer

        cd mapping
        rosrun rviz rviz -d mapping.rviz


5. Save the map

    When you are happy with the generated map, save it with    

        rosrun map_server map_saver -f <MAP_NAME>

    The origin of the map (0,0,0) is the initial pose of the robot when the mapping node is started.


