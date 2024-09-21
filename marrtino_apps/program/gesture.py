#!/usr/bin/env python

import sys,os
sys.path.append(os.getenv("MARRTINO_APPS_HOME")+"/program")

from robot_cmd_ros import *

user = None



"""Describe this function...
"""
def Zero():
    right_shoulder_flexion(0)
    left_shoulder_flexion(0)
    right_shoulder_rotation(0)
    left_shoulder_rotation(0)
    right_elbow(0)
    left_elbow(0)
    right_hand(0)
    left_hand(0)

"""Describe this function...
"""
def init2():
    right_shoulder_flexion(-70)
    left_shoulder_flexion(-70)
    right_shoulder_rotation(0)
    left_shoulder_rotation(0)
    right_elbow(0)
    left_elbow(0)
    right_hand(90)
    left_hand(90)

"""Describe this function...
"""
def init():
    right_shoulder_flexion(-70)
    left_shoulder_flexion(-70)
    right_shoulder_rotation(0)
    left_shoulder_rotation(0)
    right_elbow(0)
    left_elbow(0)
    right_hand(90)
    left_hand(90)


# Generate with blockly
begin()
Zero()
wait(4)
head_position("front")
init()
end()