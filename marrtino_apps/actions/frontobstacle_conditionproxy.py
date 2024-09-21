# wait action

import time, sys
import random, math

import rospy
from sensor_msgs.msg import LaserScan

from conditionproxy import ConditionProxy

CONDITION_NAME = 'frontobstacle'

TOPIC_scan = 'scan'

class ObstacleConditionProxy(ConditionProxy):

    def __init__(self, conditionnane):
        ConditionProxy.__init__(self, conditionnane)

        self.laser_center_dist = 0
        self.laser_left_dist = 0
        self.laser_right_dist = 0

        self.laser_sub = rospy.Subscriber(TOPIC_scan, LaserScan, self.laser_cb)


    def __del__(self):
        ConditionProxy.__del__(self)
        self.laser_sub.unregister()

    def condition_thread(self, params):
        thr = float(params)
        while self.do_run:
            if self.laser_center_dist == 0:
                self.setValue(-1)
            elif self.laser_center_dist < thr:
                self.setValue(1)
            else:
                self.setValue(0)
            rospy.sleep(0.25)

    def laser_cb(self, data):

        nc = len(data.ranges)/2
        nr = int((data.angle_max - math.pi/2)/data.angle_increment)
        nl = len(data.ranges) - nr

        dth = int((10*math.pi/180)/ data.angle_increment)

        self.laser_center_dist = min(data.ranges[nc-dth:nc+dth])
        try:
            self.laser_left_dist = min(data.ranges[nl-dth:nl+dth])
            self.laser_right_dist = min(data.ranges[nr-dth:nr+dth])
        except:
            pass
        '''
        print("angle min %.3f max %.3f inc %.6f" \
            %(data.angle_min, data.angle_max, data.angle_increment))
        print("center %.3f left %.3f right %.3f"  \
            %(self.laser_center_dist, self.laser_left_dist, self.laser_right_dist))
        '''



if __name__ == "__main__":

    params = '1.0'
    if (len(sys.argv)>1):
        params = sys.argv[1]

    obst = ObstacleConditionProxy(CONDITION_NAME)
    obst.execute(params)  # blocking, CTRL-C to interrupt


