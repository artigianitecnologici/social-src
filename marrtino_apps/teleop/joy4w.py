import sys
sys.path.append('../program')
from robot_cmd_ros import *


begin()

print('Joy4wd started.')

vel = 0.1
dt = 0.1
run = True

while (run):
    v = getJoyVel()

    vr = 1
    vl = 1
    if (v[1]>0):
        vr = +1
        vl = -1
    if (v[1]<0):
        vr = -1
        vl = +1

    fl =  vel * v[0]  * vl
    fr =  vel * v[0]  * vr
    bl =  vel * v[0]  * vl
    br =  vel * v[0]  * vr

    try:
        setSpeed4W(fl,fr,bl,br,dt)
        rospy.sleep(dt)
    except KeyboardInterrupt:
        run = False

setSpeed4W(0,0,0,0,dt)

print('Joy4wd stopped.')

end()

