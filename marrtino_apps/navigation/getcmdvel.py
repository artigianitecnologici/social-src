import math, time

import rospy
from geometry_msgs.msg import Twist

TOPIC_cmdvel = '/cmd_vel'

def cmdvel_cb(data):
    print('%.3f;%.3f' %(data.linear.x, data.angular.z))


# main
if __name__ == "__main__":

    rospy.init_node('getcmdvel', disable_signals=True)

    cmdvel_sub = rospy.Subscriber(TOPIC_cmdvel, Twist, cmdvel_cb)

    while not rospy.is_shutdown():
        time.sleep(1)

    cmdvel_sub.unregister()







