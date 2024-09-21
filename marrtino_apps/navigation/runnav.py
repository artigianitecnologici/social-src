import os
import time, math
import argparse

sessionname = 'navigation'

def send_command(cmd, name):
    print cmd
    use_tmux = False # os.system('tmux -V')==0
    
    if use_tmux:        
        r = os.system('tmux select-window -t %s:0' %sessionname)
        if r!=0:
            os.system('tmux -2 new-session -d -s %s' %sessionname)
        r = os.system('tmux select-window -t %s' %name)
        if (r!=0): # if not existing
            os.system('tmux new-window -n %s' %name)
        os.system('tmux send-keys "%s" C-m' %cmd)
    else:
        os.system('xterm -e "%s" &' %cmd)


def runnav(mapname,init_pose):

    #send_command('cd $MARRTINO_APPS_HOME/stage','stage')
    #send_command('roslaunch simrobot.launch','stage')
    #time.sleep(3)
    send_command('cd $MARRTINO_APPS_HOME/navigation','loc')
    params = 'map_name:=%s initial_pose_x:=%.2f initial_pose_y:=%.2f initial_pose_a:=%.2f' %(
                mapname,init_pose[0],init_pose[1],init_pose[2]/180*math.pi)
    send_command('roslaunch srrg_localizer.launch %s' %params,'loc')
    time.sleep(3)
    send_command('cd $MARRTINO_APPS_HOME/navigation','nav')
    send_command('roslaunch move_base_gbn.launch','nav')
    time.sleep(1)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='run navigation modules')
    parser.add_argument('mapname', type=str, help='Map name (without extensions)')
    parser.add_argument('IX', type=float, help='Initial X')
    parser.add_argument('IY', type=float, help='Initial Y')
    parser.add_argument('ITH', type=float, help='Initial Theta [deg]')

    # Example: montreal 2.5 11 0

    args = parser.parse_args()
    init_pose = [args.IX,args.IY,args.ITH]

    runnav(args.mapname,init_pose)


