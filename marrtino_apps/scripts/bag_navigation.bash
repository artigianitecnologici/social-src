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
tmux send-keys "cd $HOME/src/marrtino_apps/laser" C-m
tmux send-keys "roslaunch bags_transform.launch" C-m
sleep 1

tmux select-pane -t 1
tmux send-keys "cd $HOME/src/marrtino_apps/navigation" C-m
tmux send-keys "roslaunch amcl.launch map_name:=map" C-m
#tmux send-keys "roslaunch srrg_localizer.launch map_name:=map" C-m
sleep 1

tmux select-pane -t 2
tmux send-keys "cd $HOME/src/marrtino_apps/navigation" C-m
tmux send-keys "roslaunch move_base.launch" C-m
sleep 1

tmux select-pane -t 3
tmux send-keys "cd $HOME/src/marrtino_apps/navigation" C-m
tmux send-keys "rosrun rviz rviz -d nav.rviz" C-m
sleep 1


# window 1
tmux new-window -t $SESSION:1 -n 'Mapping'

tmux send-keys "cd $HOME/bags" C-m
tmux send-keys "rosbag play --pause --clock $1" C-m

# Set default window
tmux select-window -t $SESSION:1
tmux select-pane -t 0

# Attach to session
tmux -2 attach-session -t $SESSION

