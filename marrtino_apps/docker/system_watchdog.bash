#!/bin/bash

date

rm -f ~/log/shutdownrequest ~/log/rebootrequest ~/log/quitrequest ~/log/systemupdate ~/log/dockerrestart


# add tmux session to .bashrc
grep logincompleted ~/.bashrc

if [ $? != 0 ]; then
  echo "# check if session already exists" >> ~/.bashrc
  echo "tmux has-session -t compose 2>/dev/null" >> ~/.bashrc
  echo "" >> ~/.bashrc
  echo "if [ \$? != 0 ]; then" >> ~/.bashrc
  echo "  touch ~/log/logincompleted" >> ~/.bashrc
  echo "fi" >> ~/.bashrc
  echo "" >> ~/.bashrc
  echo "" >> ~/.bashrc
  touch ~/log/logincompleted
  sleep 10
fi

# Only for VM
# add `touch ~/log/logincompleted` at the end of .bashrc
if [ -f ~/.marrtino_vm ] || [ "$HOSTNAME" == "marrtino-VM" ]; then
  echo "Waiting for login ..."

  XORG=`ps ax | grep -c Xorg`
  while [ ! -f ~/log/logincompleted ] && [ ! "$XORG" == "2" ]; do
    sleep 3
    XORG=`ps ax | grep -c Xorg`
  done
else
  sleep 10
fi
rm -f ~/log/logincompleted

sleep 10

source start_docker.bash

sleep 10

while [ ! -f ~/log/shutdownrequest ] && [ ! -f  ~/log/rebootrequest ] && [ ! -f  ~/log/quitrequest ]; do

    sleep 5

    if [ -f  ~/log/systemupdate ]; then
      echo "System update..."
      source system_update.bash
      rm -f ~/log/systemupdate
    fi

    if [ -f  ~/log/dockerrestart ]; then
      echo "docker restart..."
      source restart_docker.bash
      rm -f ~/log/dockerrestart
    fi

done

if [ -f  ~/log/shutdownrequest ]; then
  rm -f ~/log/shutdownrequest
  echo "Shutdown..."
  sudo halt
fi

if [ -f  ~/log/rebootrequest ]; then
  rm -f ~/log/rebootrequest
  echo "Reboot..."
  sudo reboot
fi

if [ -f  ~/log/quitrequest ]; then
  rm -f ~/log/quitrequest
  echo "System watchdog quit..."
fi

