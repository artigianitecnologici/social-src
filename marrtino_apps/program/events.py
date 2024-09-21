#!/usr/bin/env python

import robot_cmd_ros
from robot_cmd_ros import *

# requires websocket_robot.py running

robot_cmd_ros.use_robot = False

begin()


while (True):
    a = event()
    if (a!=''):
        print a
    wait()

end()


