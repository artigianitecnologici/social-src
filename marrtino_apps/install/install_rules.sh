#
sudo cp ./90-webcam.rules /etc/udev/rules.d/
sudo cp ./80-marrtino.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
