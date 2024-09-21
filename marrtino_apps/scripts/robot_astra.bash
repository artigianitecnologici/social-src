#!/bin/bash
SESSION=$USER

tmux -2 new-session -d -s $SESSION

# window 0
tmux rename-window 'Robot'
tmux split-window -h
tmux select-pane -t 0
tmux send-keys "cd $HOME/src/marrtino_apps/robot" C-m
tmux send-keys "roslaunch robot.launch" C-m
sleep 3
tmux select-pane -t 1
tmux send-keys "cd $HOME/src/marrtino_apps/laser" C-m
tmux send-keys "roslaunch astra_laser.launch" C-m

# Set default window
tmux select-window -t $SESSION:0

# Attach to session
tmux -2 attach-session -t $SESSION

