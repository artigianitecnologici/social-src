# laser

Laser launchers (Hokuyo, RPlidar, RGBD depth2laser)

## Install

Note: installation is not necessary when using dockerized components.

* `ros-[kinetic/melodic]-urg-node`
* `ros-[kinetic/melodic]-laser-filters`
* `https://github.com/Slamtec/rplidar_ros.git`
* `https://bitbucket.org/ggrisetti/depth2laser`

## Configure

Check udev rule in `/etc/udev/rules.d`

Example:

    # RPLidar A1
    SUBSYSTEM=="usb", ATTR{idProduct}=="ea60", ATTR{idVendor}=="10c4", MODE:="0666", OWNER:="root", GROUP:="root" SYMLINK+="rplidar"



Adjust file `config/transforms.txt` folder for 
camera and virtual laser transforms



## Run

Launch laser or rgbdlaser nodes

    roslaunch <laser>.launch

View RGBD laser

    rosrun rviz rviz -d rgbd_laser.rviz

## Laser filter 

To use `laser_filter` 

1) configure filter parameters in `config/laser_filter.yaml`

2) launch `laser_filter.launch`

    roslaunch laser_filter.launch

3) run localization and navigation modules with option `laser_topic:=scan_filtered`


Example:

    roslaunch move_base_gbn.launch laser_topic:=scan_filtered



