#!/bin/bash
SESSION=$USER

tmux -2 new-session -d -s $SESSION

# window 0
tmux rename-window 'Robot'
tmux split-window -h
tmux select-pane -t 0
tmux send-keys "cd $HOME/src/marrtino_apps/stage" C-m
tmux send-keys "roslaunch simrobot.launch" C-m
sleep 1

tmux select-pane -t 1
tmux split-window -v
tmux select-pane -t 1
tmux send-keys "cd $HOME/src/marrtino_apps/laser" C-m
tmux send-keys "roslaunch astra_laser.launch" C-m
sleep 1

tmux select-pane -t 2
tmux send-keys "cd $HOME/src/marrtino_apps/teleop" C-m
tmux send-keys "roslaunch teleop.launch use_joystick:=false" C-m

# window 1
#tmux new-window -t $SESSION:1 -n 'Teleop'

# Set default window
tmux select-window -t $SESSION:0

# Attach to session
tmux -2 attach-session -t $SESSION

