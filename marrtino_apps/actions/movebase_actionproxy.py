# transform move_base string to move_base goal

import time, math, sys

import rospy
import tf

import actionlib
from actionlib_msgs.msg import *

from geometry_msgs.msg import Quaternion, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionproxy import ActionProxy

ACTION_NAME = 'movebase'        # PNP action
ACTION_move_base = 'move_base'  # ROS action
TOPIC_amcl_pose = 'amcl_pose'   # localizer pose


class MoveBaseActionProxy(ActionProxy):

    def __init__(self,actionname):
        ActionProxy.__init__(self,actionname)
        self.ac_movebase = None
        self.map_robot_pose = [0,0,0]

    def target_params(self, params):
        v = params.split('_')
        return [float(v[0]), float(v[1]), float(v[2])]


    def getRobotPose(self):
        return self.map_robot_pose

    def localizer_cb(self, data):
        self.map_robot_pose[0] = data.pose.pose.position.x
        self.map_robot_pose[1] = data.pose.pose.position.y
        o = data.pose.pose.orientation
        q = (o.x, o.y, o.z, o.w)
        euler = tf.transformations.euler_from_quaternion(q)
        self.map_robot_pose[2] = euler[2] # yaw

    def send_goal(self, target_pose):

        if self.ac_movebase == None:
            self.ac_movebase = actionlib.SimpleActionClient(ACTION_move_base,MoveBaseAction)

        self.ac_movebase.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = target_pose[0]
        goal.target_pose.pose.position.y = target_pose[1]
        yaw = target_pose[2]/180.0*math.pi
        q = tf.transformations.quaternion_from_euler(0, 0, yaw)
        goal.target_pose.pose.orientation = Quaternion(q[0],q[1],q[2],q[3])

        self.ac_movebase.send_goal(goal)

        rospy.loginfo("move_base: goal %r sent!" %(target_pose))


    def action_thread(self, params): 

        self.loc_sub = rospy.Subscriber(TOPIC_amcl_pose, PoseWithCovarianceStamped, self.localizer_cb)

        target_pose = self.target_params(params)
        self.send_goal(target_pose)

        finished = False
        while self.do_run and not finished:
            self.ac_movebase.wait_for_result(rospy.Duration(1))
            status = self.ac_movebase.get_state() # 1 ACTIVE, 3 SUCCEEDED  http://docs.ros.org/en/api/actionlib_msgs/html/msg/GoalStatus.html
            result = self.ac_movebase.get_result() 
            
            #print("%r %r" %(status,result))
            finished = status == GoalStatus.SUCCEEDED

        state = self.ac_movebase.get_state()
        if state == GoalStatus.SUCCEEDED:
            rospy.loginfo("move_base: goal succeeded!")
        else:
            rospy.loginfo("move_base: goal failed!")

        self.ac_movebase.get_result()

        self.ac_movebase.cancel_all_goals()

        self.loc_sub.unregister()


if __name__ == "__main__":

    params = None
    if (len(sys.argv)>1):
        params = sys.argv[1]

    move = MoveBaseActionProxy(ACTION_NAME)

    if params is not None:
        move.execute(params)  # blocking, CTRL-C to interrupt
    else:
        move.run_server()     # blocking, CTRL-C to interrupt

