#!/usr/bin/env python

import sys,os
sys.path.append(os.getenv("MARRTINO_APPS_HOME")+"/program")

from robot_cmd_ros import *

user = None

def init():
  right_shoulder_flexion(-70)
  left_shoulder_flexion(-70)
  right_shoulder_rotation(0)
  left_shoulder_rotation(0)
  right_elbow(0)
  left_elbow(0)
  right_hand(90)
  left_hand(90)

begin()
init()
head_position("front")
emotion("normal")
emotion("speak")
say('My name is martina and you ?','en')
emotion("normal")
for count in range(2):
  user = wait_get_user_say()
  if user != '':
    print(user)
    emotion("speak")
    say('ciao','it')
    say(user,'it')
    emotion("normal")
end()

