#!/bin/bash
SESSION=$USER

tmux -2 new-session -d -s $SESSION

# window 0
tmux rename-window 'Robot'

tmux split-window -v
tmux select-pane -t 0
tmux split-window -h
tmux select-pane -t 2
tmux split-window -h

tmux select-pane -t 0
tmux send-keys "cd $HOME/src/marrtino_apps/robot" C-m
tmux send-keys "roslaunch robot.launch" C-m
sleep 3

tmux select-pane -t 1
tmux send-keys "cd $HOME/src/marrtino_apps/teleop" C-m
tmux send-keys "roslaunch teleop.launch use_joystick:=true" C-m
sleep 1

tmux select-pane -t 2
tmux send-keys "cd $HOME/src/marrtino_apps/laser" C-m
tmux send-keys "roslaunch hokuyo.launch" C-m
#tmux send-keys "roslaunch astra_laser.launch" C-m
#tmux send-keys "roslaunch xtion_laser.launch" C-m
sleep 1


# window 1
tmux new-window -t $SESSION:1 -n 'Bag'

tmux select-pane -t 0
tmux send-keys "cd $HOME/bags" C-m
tmux send-keys "rosbag record -o mybag /odom /scan" 
sleep 1

tmux select-window -t $SESSION:1

# Attach to session
tmux -2 attach-session -t $SESSION

