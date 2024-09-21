# transform move_base string to move_base goal

import time, math, sys

import rospy
import tf

from geometry_msgs.msg import Twist, Quaternion, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from actionproxy import ActionProxy

ACTION_NAME = 'turn'        # PNP action

TOPIC_odom = 'odom'             # odom pose
TOPIC_amcl_pose = 'amcl_pose'   # localizer pose
TOPIC_cmd_vel = 'cmd_vel'
TOPIC_desired_cmd_vel = 'desired_cmd_vel'

def NORM_PI(a):
    if (a>math.pi):
        return a-2*math.pi
    elif (a<-math.pi):
        return a+2*math.pi
    else:
        return a

def DEG2RAD(a):
    return a*math.pi/180.0

def RAD2DEG(a):
    return a/math.pi*180.0


class TurnActionProxy(ActionProxy):

    def __init__(self,actionname):
        ActionProxy.__init__(self,actionname)
        self.map_robot_pose = [0,0,0]
        self.odom_robot_pose = [0,0,0]
        self.stop_request = False

    def target_params(self, params):  # <degree>_[ABS|REL]
        v = params.split('_')
        return [float(v[0]), v[1]]


    def getRobotPose(self):
        return self.map_robot_pose


    def odom_cb(self, data):
        self.odom_robot_pose[0] = data.pose.pose.position.x
        self.odom_robot_pose[1] = data.pose.pose.position.y
        o = data.pose.pose.orientation
        q = (o.x, o.y, o.z, o.w)
        euler = tf.transformations.euler_from_quaternion(q)
        self.odom_robot_pose[2] = euler[2] # yaw
    
    def localizer_cb(self, data):
        self.map_robot_pose[0] = data.pose.pose.position.x
        self.map_robot_pose[1] = data.pose.pose.position.y
        o = data.pose.pose.orientation
        q = (o.x, o.y, o.z, o.w)
        euler = tf.transformations.euler_from_quaternion(q)
        self.map_robot_pose[2] = euler[2] # yaw


    def setSpeed(self,lx,az,tm,stopend=False):
        if (self.stop_request and (lx!=0.0 or az!=0.0)):
            raise Exception("setSpeed called in stop_request mode")

        delay = 0.1 # sec
        rate = rospy.Rate(1/delay) # Hz
        cnt = 0.0
        msg = Twist()
        msg.linear.x = lx
        msg.angular.z = az
        msg.linear.y = msg.linear.z = msg.angular.x = msg.angular.y =  0
        while not rospy.is_shutdown() and cnt<=tm and not self.stop_request:
            self.cmd_pub.publish(msg)
            cnt = cnt + delay
            try:
                rate.sleep()
            except KeyboardInterrupt:
                print("User KeyboardInterrupt")
                return False
        if (stopend):
            msg.linear.x = 0
            msg.angular.z = 0
            self.cmd_pub.publish(msg)
            rate.sleep()
        return True




    def turnto_goal(self,target_pose):

        print('Turn to goal')

        r = True

        p = self.getRobotPose()

        if math.fabs(target_pose[1]-p[1]) + math.fabs(target_pose[0]-p[0]) < 0.5:
            return True

        ad = math.atan2(target_pose[1]-p[1],target_pose[0]-p[0])
        th_deg = (ad-p[2])*180/math.pi 
        if math.fabs(th_deg)>30:
            r = turn(th_deg)

        return r


    def get_current_th(self,frame):
        if frame=='ABS':
            return self.map_robot_pose[2]
        else: # 'REL'
            return self.odom_robot_pose[2]


    def action_thread(self, params): 

        rv_good = 1.0 
        rv_min = 0.5

        self.odom_sub = rospy.Subscriber(TOPIC_odom, Odometry, self.odom_cb)
        self.localizer_sub = rospy.Subscriber(TOPIC_amcl_pose, PoseWithCovarianceStamped, self.localizer_cb)
        self.cmd_pub = rospy.Publisher(TOPIC_cmd_vel, Twist, queue_size=1)
        
        rospy.sleep(0.5) # wait for some messages...

        target = self.target_params(params)
        target_th = DEG2RAD(target[0])  # rad
        current_th = self.odom_robot_pose[2]
        if target[1]=='REL':
            target_th = NORM_PI(target_th + current_th)
        else: # 'ABS'
            target_th = NORM_PI(target_th - self.map_robot_pose[2] + self.odom_robot_pose[2])
        # now target_th is an absolute target angle in odom frame

        print("TURN -- map th: %.1f odom th: %.1f" \
            %(RAD2DEG(self.map_robot_pose[2]), RAD2DEG(self.odom_robot_pose[2])))

        print("TURN -- th: %.1f -- target: %.1f" %(RAD2DEG(current_th), RAD2DEG(target_th)))
        #print("TURN -- to-normalize RAD: %.1f" %(current_th + target_th))
        #target_th = norm_target_angle(current_th + target_th)
        #print("TURN -- currentTh: %.1f -- targetTh %.1f" %(RAD2DEG(current_th), RAD2DEG(target_th)))


        dth = abs(NORM_PI(target_th-current_th))

        rv_nom = rv_good 
        if (NORM_PI(target_th-current_th) < 0):
            rv_nom *= -1

        # turn loop

        print("TURN -- dTh %.2f abs norm_PI: %.2f" %(target_th-current_th,dth))

        last_dth = dth
        #print("TURN -- last_dth %.2f" %(last_dth))

        while self.do_run and (dth>rv_min/8.0 and last_dth>=dth):
            rv = rv_nom
            if (dth<0.8):
                rv = rv_nom*dth/0.8
            if (abs(rv)<rv_min):
                rv = rv_min*rv/abs(rv)
            tv = 0.0
            if self.setSpeed(tv, rv, 0.1, False):
                current_th = self.odom_robot_pose[2]
                dth = abs(NORM_PI(target_th-current_th))
                if (dth < last_dth or dth>0.3): # to avoid oscillation close to 0
                    last_dth = dth
            else:
                print("turn action canceled by user")
                r = False
                dth=0
            print("TURN -- th: %.1f -- target: %.1f  dth %.2f -- VEL: %.2f %.2f" \
                %(RAD2DEG(current_th), RAD2DEG(target_th), RAD2DEG(dth), tv, rv))


        #print("TURN -- dth %.2f - last_dth %.2f" %(dth,last_dth))
        self.setSpeed(0.0,0.0,0.1)
        print('TURN -- end')


        self.odom_sub.unregister()
        self.localizer_sub.unregister()


if __name__ == "__main__":

    params = None
    if (len(sys.argv)>1):
        params = sys.argv[1]

    turn = TurnActionProxy(ACTION_NAME)

    if params is not None:
        turn.execute(params)  # blocking, CTRL-C to interrupt
    else:
        turn.run_server()     # blocking, CTRL-C to interrupt

