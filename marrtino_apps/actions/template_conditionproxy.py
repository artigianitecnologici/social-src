# template condition

import sys

from conditionproxy import ConditionProxy

CONDITION_NAME = 'template'    # <--- condition name

class TemplateConditionProxy(ConditionProxy):   # <--- condition class

    def __init__(self, conditionnane):
        ConditionProxy.__init__(self, conditionnane)
                                                # <--- condition init


    def __del__(self):
        ConditionProxy.__del__(self)
                                                # <--- condition del


    def condition_thread(self, params):
                                                # <--- condition params

        while self.do_run:
                                                # <--- condition loop
            rospy.sleep(0.25)

                                                # <--- condition end




if __name__ == "__main__":

    params = ''
    if (len(sys.argv)>1):
        params = sys.argv[1]

    t = TemplateConditionProxy(CONDITION_NAME)
    t.execute(params)  # blocking, CTRL-C to interrupt


