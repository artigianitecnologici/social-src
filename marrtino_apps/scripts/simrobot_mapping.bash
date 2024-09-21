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
tmux send-keys "cd $HOME/src/marrtino_apps/stage" C-m
tmux send-keys "roslaunch simrobot.launch" C-m
sleep 3

tmux select-pane -t 1
tmux send-keys "cd $HOME/src/marrtino_apps/mapping" C-m
tmux send-keys "rosrun rviz rviz -d mapping.rviz" C-m
sleep 1

tmux select-pane -t 2
tmux send-keys "cd $HOME/src/marrtino_apps/mapping" C-m
tmux send-keys "roslaunch srrg_mapper.launch" C-m
#tmux send-keys "roslaunch gmapping.launch" C-m
sleep 1

tmux select-pane -t 3
tmux send-keys "cd $HOME/src/marrtino_apps/navigation" C-m
tmux send-keys "roslaunch move_base.launch" C-m
sleep 1


# window 1
tmux new-window -t $SESSION:1 -n 'Mapping'

tmux send-keys "cd $HOME/src/marrtino_apps/teleop" C-m
tmux send-keys "roslaunch teleop.launch use_joystick:=false" C-m
sleep 1

tmux split-window -v

tmux send-keys "cd $HOME/src/marrtino_apps/mapping/maps" C-m
tmux send-keys "rosrun map_server map_saver -f mymap"
sleep 1

# Set default window
tmux select-window -t $SESSION:1

# Attach to session
xterm -e "tmux -2 attach-session -t $SESSION" &

