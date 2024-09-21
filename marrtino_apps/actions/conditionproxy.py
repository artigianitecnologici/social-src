#
# ConditionProxy base class
#

from threading import Thread

import rospy
from std_msgs.msg import String

'''
pnp_ros reads conditions from ROS params named `pnp/conditionsBuffer/<condition>` with values

     1: True
     0: False
    -1: unknown


Condition executors should set these values.

Test with CLI

    rosparam get pnp/conditionsBuffer/<condition>

    rosparam set pnp/conditionsBuffer/<condition> 1

Quit all proxies with

    rostopic pub pnp/action_str std_msgs/String "data: '%quit_server'" --once

'''


# topic for subscribers
TOPIC_PNPACTIONPROXY_STR = "pnp/action_str"

# param for conditions
PARAM_PNPCONDITIONBUFFER = "pnp/conditionsBuffer/"


class ConditionProxy:

    def __init__(self, conditionname):

        self.conditionname = conditionname
        self.timestamp = None   # time of current value
        self.value = None       # current value
        self.cthread = None
        self.param = PARAM_PNPCONDITIONBUFFER + conditionname

        # init ROS node
        nodename = conditionname+"_conditionproxy"
        rospy.init_node(nodename,  disable_signals=True)

        # subscribers
        self.actionproxy_sub = rospy.Subscriber(TOPIC_PNPACTIONPROXY_STR, String, self.actionproxy_cb)  # only to check quit signal


    def __del__(self):
        # just in case
        self.end()

    def actionproxy_cb(self, data):
        sdata = data.data
        if ('%quit_server' in sdata):
            self.end()
            


    def start(self, params=None):
        if self.cthread != None:
            self.end()
        self.do_run = True
        self.cthread = Thread(target=self.condition_thread, args=(params,))
        self.cthread.start()

    def end(self):
        self.do_run = False
        if self.cthread != None:
            self.cthread.join()
        self.cthread = None

    def interrupt(self):
        self.end()

    def isRunning(self):
        self.do_run = self.cthread != None and self.cthread.is_alive()
        return self.do_run

    def setValue(self, value):  # 1: true,  0: false,  -1: unknown
        self.lasttime = rospy.Time.now()
        rospy.set_param(self.param, value)

    def getValue(self):
        v = -1
        try:
            v = rospy.get_param(self.param)
        except:
            pass
        return v

    def execute(self, params):
        print("ConditionProxy %s running ..." %(self.conditionname))

        self.start(params)
        while (self.isRunning()):
            try:
                #print("%s = %d" %(self.conditionname, self.getValue()))
                rospy.sleep(1)
            except KeyboardInterrupt:
                print("ConditionProxy %s - user interrupt" %(self.conditionname))
                self.interrupt()
        self.end()

        print("ConditionProxy %s quit" %(self.conditionname))


    def condition_thread(self, params):
        pass




