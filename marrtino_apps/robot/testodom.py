import rospy
import tf

from nav_msgs.msg import Odometry

odom_robot_pose = None
odom_robot_vel = None

def odom_cb(data):
    global odom_robot_pose, odom_robot_vel
    print("!!! odom cb !!!")
    if (odom_robot_pose is None):
        odom_robot_pose = [0,0,0]
    odom_robot_pose[0] = data.pose.pose.position.x
    odom_robot_pose[1] = data.pose.pose.position.y
    o = data.pose.pose.orientation
    q = (o.x, o.y, o.z, o.w)
    euler = tf.transformations.euler_from_quaternion(q)
    odom_robot_pose[2] = euler[2] # yaw
    #odomframe = data.header.frame_id


rospy.init_node('testodom',  disable_signals=True)

rospy.sleep(1)

TOPIC_odom = 'odom'

odom_sub = rospy.Subscriber(TOPIC_odom, Odometry, odom_cb)

delay = 0.25 # sec
rate = rospy.Rate(1/delay) # Hz
try:
    rate.sleep()
    timeout = 10 #seconds
    while (odom_robot_pose is None and timeout>0):
        rate.sleep()
        timeout -= delay
except KeyboardInterrupt:
    pass

print(odom_robot_pose)



