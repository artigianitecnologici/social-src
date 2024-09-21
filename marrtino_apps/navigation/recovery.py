import os,sys 
from actionlib_msgs.msg import GoalStatus, GoalStatusArray
from move_base_msgs.msg import MoveBaseActionGoal
from nav_msgs.msg import Odometry
import tf

sys.path.append(os.getenv('MARRTINO_APPS_HOME')+'/program')

from robot_cmd_ros import *
from getpose import *

TOPIC_movebase_goal = 'move_base/goal'
TOPIC_movebase_status = 'move_base/status'
TOPIC_cmd_vel = '/cmd_vel'

# spqrel_planner
TOPIC_planner_state = 'planner_state'

recovery = False  # when to do recovery

# goal map (map of GoalStatus)
Goals = {}

# global status
target_goal = [0,0,0]
goal_active = False
robot_moving = False
recovery_cnt = 0

def log(message):
    tm = rospy.get_time()
    p = get_robot_pose()
    print("%.2f;%s;%s" %(tm,pose_str(p),message))


def planner_state_cb(msg):
    global recovery
    if (msg.data!='running' and msg.data!='aborted'):
        #print msg.data
        pass
    if 'recovery' in msg.data:
        recovery = True

def movabase_goal_cb(msg):
    global target_goal
    target_goal[0] = msg.goal.target_pose.pose.position.x
    target_goal[1] = msg.goal.target_pose.pose.position.y
    o = msg.goal.target_pose.pose.orientation
    q = (o.x, o.y, o.z, o.w)
    euler = tf.transformations.euler_from_quaternion(q)
    target_goal[2] = euler[2] # yaw

def movabase_status_cb(msg):
    global goal_active, target_goal
    if len(msg.status_list)>0:
      for d in msg.status_list:
        gid = d.goal_id.id
        if not gid in Goals.keys() or Goals[gid].status!=d.status:
            log("Goal;%s;%d;%s" %(pose_str(target_goal), d.status, d.text))
        Goals[gid] = d
        if (d.status==1): # goal accepted
            goal_active = True
        elif (d.status==2): # goal aborted
            goal_active = False
        elif (d.status==3): # goal reached
            goal_active = False


def odom_cb(data):
    global robot_moving
    vx = data.twist.twist.linear.x
    vth = data.twist.twist.angular.z
    if (math.fabs(vx)<0.01 and math.fabs(vth)<0.01):
      robot_moving = False
    else:
      #print("%.1f %.2f" %(vx,vth))
      robot_moving = True


def recovery():
    global goal_active, robot_moving, recovery_cnt
    r = goal_active and not robot_moving
    if r:
        recovery_cnt += 1
    else:
        recovery_cnt = 0
    return r


def do_recovery1():
    log("Recovery1;start")
    enableObstacleAvoidance(True)
    setSpeed(-0.1,0,3.0) # backward
    setSpeed(0.2,0,6.0) # forward
    enableObstacleAvoidance(False)
    log("Recovery1;end")


def do_recovery():
    global target_goal, recovery_cnt
    recovery_max = 5
    if recovery_cnt>1:
        log("Recovery;%d/%d"  %(recovery_cnt,recovery_max))
    if recovery_cnt>recovery_max:
        do_recovery1()





begin(nodename='recovery')

odom_sub = rospy.Subscriber(TOPIC_odom, Odometry, odom_cb)
goal_sub = rospy.Subscriber(TOPIC_movebase_goal, MoveBaseActionGoal, movabase_goal_cb)
status_sub = rospy.Subscriber(TOPIC_movebase_status, GoalStatusArray, movabase_status_cb)

run = True
while marrtino_ok() and run:
  if recovery():
    do_recovery()
  try:
    time.sleep(0.25)
  except KeyboardInterrupt:
    run = False

odom_sub.unregister()
goal_sub.unregister()
status_sub.unregister()

end()

