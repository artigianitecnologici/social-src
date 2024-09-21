#!/bin/bash

SESSION=init

# Set up session
tmux -2 new-session -d -s $SESSION
tmux rename-window -t $SESSION:0 'server'
tmux new-window -t $SESSION:1 -n 'cmd'

tmux send-keys -t $SESSION:0 "cd /home/robot/src/marrtino_apps/vision/" C-m
tmux send-keys -t $SESSION:0 "python mobilenet_objrec.py  --server" C-m


while [ ! -f "/tmp/quitrequest" ]; do
  sleep 5
done

