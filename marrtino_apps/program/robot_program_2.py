#!/usr/bin/env python

import sys,os
sys.path.append(os.getenv("MARRTINO_APPS_HOME")+"/program")

import robot_cmd_ros
from robot_cmd_ros import *

robot_cmd_ros.use_robot = True

begin()

# Wait until a tag or an obstacle is detected 
while (not tag_trigger() and laser_center_distance()>1.0 ):	
	bip()
	wait()

# Print information
print 'Laser distance: ', laser_center_distance()
print 'Tag detected: ',tag_id(),' distance: ',tag_distance()

bop()

end()


