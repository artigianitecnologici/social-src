# Autostart 

To start devices and functionalities at boot automatically

1. Copy `autostart.yaml` file from template

        cd $MARRTINO_APPS_HOME
        cp start/autostart_template.yaml ./autostart.yaml

2. Edit `autostart.yaml` and choose the configuration you want to run

3. Start (or restart) docker

        cd $MARRTINO_APPS_HOME/docker
        ./start_docker.bash

This autostart will work also at robot boot.


## Manual start

Edit a start file `mystart.yaml`

Manual start

        cd $MARRTINO_APPS_HOME/start
        python autostart.py mystart.yaml

Manual quit

        cd $MARRTINO_APPS_HOME/start
        python autostart.py mystart.yaml --kill




