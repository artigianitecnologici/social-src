#!/usr/bin/env python

import sys,os
sys.path.append(os.getenv("MARRTINO_APPS_HOME")+"/program")

from robot_cmd_ros import *

begin()

bip()

wait()

forward(2)
backward()
left(2)
forward(1)
right(2)

wait()

bop()

stop()

end()



