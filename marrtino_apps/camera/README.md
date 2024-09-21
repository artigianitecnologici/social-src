# camera #

Camera launchers: usbcam/xtion/astra sensor

Important: plug cameras in direct USB ports (not to hubs).

## Install ##

Note: installation is not necessary when using dockerized components.


Download the following packages in your catkin workspace and compile them with catkin_make:

Astra:

* https://github.com/tfoote/ros_astra_camera.git

Xtion:

* ros-kinetic-openni2-camera
* ros-kinetic-openni2-launch



## Run ##

* Run usbcam/xtion/astra node

Launch

    roslaunch astra.launch [viewimage:=true] [videoserver:=true]

or

    roslaunch usbcam.launch [viewimage:=true] [videoserver:=true]

or

    roslaunch xtion2.launch


To visualize images and depth data

    rosrun image_view image_view image:=/rgb/image_raw

If using videoserver

    http://localhost:9090/

Note: To visualize images from another PC, export ROS_MASTER_URI. This feature may be very slow specially if using a wireless network.

## Sending images to classification servers 

    rostopic pub  /takephoto ...  "send <server> <port> [<width> <height>]"



