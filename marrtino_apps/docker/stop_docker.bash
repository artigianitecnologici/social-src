#!/bin/bash

SESSION=compose


tmux send-keys -t $SESSION:4 "cd \$MARRTINO_APPS_HOME/start" C-m
tmux send-keys -t $SESSION:4 "python3 autostart.py --kill" C-m

sleep 10

tmux send-keys -t $SESSION:1 "cd \$MARRTINO_APPS_HOME/docker && docker-compose down" C-m


if [ -f /tmp/marrtinosocialon ] && [ "$MARRTINO_SOCIAL" != "" ]; then

  tmux send-keys -t $SESSION:3 "cd \$MARRTINO_SOCIAL/docker && docker-compose down" C-m

fi

tmux send-keys -t $SESSION:1 "docker container prune -f" C-m


