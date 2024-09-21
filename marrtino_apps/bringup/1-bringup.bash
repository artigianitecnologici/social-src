#!/bin/bash

# launched by marrtino:base container

date

if [ "$MARRTINO_APPS_HOME" == "" ]; then
  export MARRTINO_APPS_HOME=$HOME/src/marrtino_apps
fi

if [ "$MODIM_HOME" == "" ]; then
  export MODIM_HOME=$HOME/src/modim
fi


#source $HOME/.bashrc
source $HOME/ros/catkin_ws/devel/setup.bash
#export DISPLAY=:0
#export ROBOT_TYPE=marrtino

mkdir -p $HOME/log

SESSION=init

# check if session already exists
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  # Set up your session
  tmux -2 new-session -d -s $SESSION
  tmux rename-window -t $SESSION:0 'config'
  tmux new-window -t $SESSION:1 -n 'bringup'
  tmux new-window -t $SESSION:2 -n 'roscore'
  tmux new-window -t $SESSION:3 -n 'wsrobot'
fi

tmux send-keys -t $SESSION:0 "cd \$MARRTINO_APPS_HOME/config" C-m
tmux send-keys -t $SESSION:0 "python wsconfig.py" C-m

tmux send-keys -t $SESSION:1 "cd \$MARRTINO_APPS_HOME/bringup" C-m
tmux send-keys -t $SESSION:1 "python wsbringup.py" C-m

tmux send-keys -t $SESSION:2 "roscore" C-m

sleep 5

tmux send-keys -t $SESSION:3 "cd \$MARRTINO_APPS_HOME/blockly" C-m
tmux send-keys -t $SESSION:3 "python websocket_robot.py" C-m

while [ ! -f "/tmp/quitrequest" ]; do
  sleep 5
done

