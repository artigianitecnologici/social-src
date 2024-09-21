import sys,os,time
import argparse

sys.path.append(os.getenv("MARRTINO_APPS_HOME")+"/program")

import robot_cmd_ros
from robot_cmd_ros import *

robot_cmd_ros.use_audio = False
robot_cmd_ros.tv_good = 0.5

import move


def moveTo(px,py,pth=1001):
    return move.do_move([px,py,pth])

def do_path(filename):
    with open(filename) as f:
        l = f.readline()
        r = True
        while r and l!='':
            v = l.split("#")
            p = v[0].strip()
            if len(p)>0:
                print(p)
                r = eval(p)
            l = f.readline()

        return r



# main
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='navigator')
    parser.add_argument('path', type=str, help='File with path to run')

    args = parser.parse_args()

    begin(nodename='navigator')
    enableObstacleAvoidance(True)

    r = do_path(args.path)
    print("Path completed: %r" %r)

    end()


