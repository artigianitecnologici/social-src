#!/bin/bash

# arduino, ln298, pka03, marrtino2019

MB="marrtino2019"
if [ "$1" != "" ]; then
  MB="$1"
fi

echo "load_config ${MB}_firmware_params.cfg" > /tmp/upload_config.script
echo "send system_params" >> /tmp/upload_config.script
echo "send joint_params[0]" >> /tmp/upload_config.script
echo "send joint_params[1]" >> /tmp/upload_config.script
echo "send joint_params[2]" >> /tmp/upload_config.script
echo "send joint_params[3]" >> /tmp/upload_config.script
echo "send drive_params" >> /tmp/upload_config.script
echo "send sonar_params" >> /tmp/upload_config.script
echo "store system_params" >> /tmp/upload_config.script
echo "store joint_params[0]" >> /tmp/upload_config.script
echo "store joint_params[1]" >> /tmp/upload_config.script
echo "store joint_params[2]" >> /tmp/upload_config.script
echo "store joint_params[3]" >> /tmp/upload_config.script
echo "store drive_params" >> /tmp/upload_config.script
echo "store sonar_params" >> /tmp/upload_config.script
echo "quit" >> /tmp/upload_config.script

cat /tmp/upload_config.script | rosrun srrg2_orazio orazio -serial-device /dev/orazio 

