# Marker detection #


## Install ##

Note: installation is not necessary when using dockerized components.

Download the following packages in your catkin workspace and compile them with catkin_make:

```
https://bitbucket.org/iocchi/apriltags_ros
```

For USB camera, install ROS nodes

```
sudo apt-get install ros-kinetic-usb-cam ros-kinetic-image-view ros-kinetic-cv-bridge 
```

Note: if you get errors in linked libraries, you may need to recompile ros packages, since this update may change the version of OpenCV libraries.


## Run ##

* Write and run your Python program (see robot_program_1.py as an example).

```
$ roslaunch xtion_tags.launch
```

* Detections are published in the ROS topic /tag_detections

```
detections: 
  - 
    id: 3
    size: 0.162
    pose: 
      header: 
        seq: 316
        stamp: 
          secs: 1495523075
          nsecs: 310249864
        frame_id: camera_frame_rgb
      pose: 
        position: 
          x: 0.0493399555915
          y: -0.168291373984
          z: 0.646280017666
        orientation: 
          x: -0.675589050172
          y: 0.725935936241
          z: -0.128485009517
          w: -0.00938371414564
---

```


