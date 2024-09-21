# autostart localizer

from __future__ import print_function

import sys, os, time, math
import rospy
import rosnode
import tf

from nav_msgs.msg import Odometry

TOPIC_GROUND_TRUTH = '/base_pose_ground_truth'

def get_ROS_nodes():
    nodes = None
    try:
        nodes = rosnode.get_node_names()
    except Exception as e:
        print(e)
    return nodes

def noderunning(nodename):
    nodes = get_ROS_nodes()
    #print(nodes)
    return nodename in nodes

gt_robot_pose = None

def groundtruth_cb(data):
    global gt_robot_pose
    if gt_robot_pose is None:
        gt_robot_pose = [0,0,0]
    gt_robot_pose[0] = data.pose.pose.position.x
    gt_robot_pose[1] = data.pose.pose.position.y
    o = data.pose.pose.orientation
    q = (o.x, o.y, o.z, o.w)
    euler = tf.transformations.euler_from_quaternion(q)
    gt_robot_pose[2] = euler[2] # yaw



### main ###

def main(argv):
    global gt_robot_pose

    rospy.init_node('autostart_localizer')

    #check if stageros is running
    stagerun = noderunning('/stageros')
    print('stageros running: %r' %(stagerun))

    #check if map_server already running
    msrun = noderunning('/map_server')
    print('map_server running: %r' %(msrun))

    # get map name
    mapname = 'map' # default map name
    if len(argv)>1:
        mapname = argv[1] # map name
    else:
        try:
            mapname = rospy.get_param('/mapname')
        except:
            pass
    print('map name: %s' %mapname)

    if not msrun:
        #   check if mapname file exists - if not ERROR
        print("TODO: check if map file %s exists" %mapname)



    #get robot current pose from topic /base_pose_ground_truth
    gt_sub = rospy.Subscriber(TOPIC_GROUND_TRUTH, Odometry, groundtruth_cb)

    print("Waiting for ground truth pose...")
    rospy.sleep(1)

    gt_sub.unregister()

    if gt_robot_pose is None and len(argv)>4:
        gt_robot_pose = [ float(argv[2]), float(argv[3]), float(argv[4])/180.0*math.pi ]

    print("Current robot pose: %r" %(gt_robot_pose))

    #start localizer
    if (msrun and stagerun):
        rstr = "roslaunch amcl.launch use_mapserver:=false "
    else:
        rstr = "roslaunch amcl.launch map_name:=%s use_mapserver:=true " %mapname

    if gt_robot_pose is not None:
        rstr += " initial_pose_x:=%.1f initial_pose_y:=%.1f  initial_pose_a:=%.3f" \
            %(gt_robot_pose[0], gt_robot_pose[1], gt_robot_pose[2])

    print(rstr)
    os.system(rstr)


# Use startloc.py [<mapname>] [<x> <y> <th_deg>]

if __name__=='__main__':
    main(sys.argv)

