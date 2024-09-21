#!/bin/bash
SESSION=$USER

tmux -2 new-session -d -s $SESSION

# window 0
tmux rename-window 'Robot'

tmux split-window -v
tmux split-window -v

tmux select-pane -t 0
tmux send-keys "cd $HOME/src/marrtino_apps/stage" C-m
tmux send-keys "roslaunch simrobot.launch" C-m
sleep 1

tmux select-pane -t 1
tmux send-keys "cd $HOME/src/marrtino_apps/teleop" C-m
tmux send-keys "roslaunch teleop.launch use_joystick:=false" C-m
sleep 1

tmux select-pane -t 2
tmux send-keys "cd $HOME/bags" C-m
tmux send-keys "rosbag record -o mybag /odom /scan" 
sleep 1

# Attach to session
tmux -2 attach-session -t $SESSION

