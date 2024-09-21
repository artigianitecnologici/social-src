# docker configuration

Follow instructions in [docker folder](https://bitbucket.org/iocchi/marrtino_apps/src/master/docker/)



# udev configuration

Copy file `80-marrtino.rules` in `/etc/udev/rules.d/`

Check Vendor and Product IDs of your devices with command `lsusb`

Edit  `/etc/udev/rules.d/80-marrtino.rules` if needed

Restart the system and enjoy!

# system_watchdog configuration

To start docker containers at boot, copy file `system_watchdog` in
`/etc/init.d`
sudo cp system_watchdog /etc/init.d/system_watchdog

Edit `/etc/init.d/system_watchdog` if needed (`user` and `dir` info)

Enable the service

    sudo systemctl enable system_watchdog

Start the service

    sudo systemctl start system_watchdog

Restart the system and enjoy!

# orazio configuration




# MARRtino firmware parameters configuration #

NOTE: Instructions have been updated for 2018 firmware. 
If you have 2017 firmware, please use the scripts named with 2017
or refer to previous checkout ```19c4c221f81e2414651aceeba900ca3a0c66988e``` of this repository.

## Scripted version ##


* to upload firmware parameters from file to Arduino


        ./uploadfirmwareparams.bash [marrtino2019|pka03|ln298|arduino]


* to download firmware parameters from Arduino to file


        cat download_config.script | rosrun srrg2_orazio orazio -serial-device /dev/orazio 



Note: change file names in the .script files if needed.



## Manual version ##


* Download

        rosrun srrg2_orazio orazio -serial-device /dev/orazio
        orazio> fetch system_params
        orazio> fetch joint_params[0]
        orazio> fetch joint_params[1]
        orazio> fetch joint_params[2]
        orazio> fetch joint_params[3]
        orazio> fetch drive_params
        orazio> fetch sonar_params
        orazio> request system_params
        orazio> request joint_params[0]
        orazio> request joint_params[1]
        orazio> request joint_params[2]
        orazio> request joint_params[3]
        orazio> request drive_params
        orazio> request sonar_params
        orazio> save_config XXX_firmware_params.cfg
        orazio> quit


* Upload

        rosrun srrg2_orazio orazio -serial-device /dev/orazio
        orazio> load_config XXX_firmware_params.cfg
        orazio> send system_params
        orazio> send joint_params[0]
        orazio> send joint_params[1]
        orazio> send joint_params[2]
        orazio> send joint_params[3]
        orazio> send drive_params
        orazio> send sonar_params
        orazio> store system_params
        orazio> store joint_params[0]
        orazio> store joint_params[1]
        orazio> store joint_params[2]
        orazio> store joint_params[3]
        orazio> store drive_params
        orazio> store sonar_params
        orazio> quit

