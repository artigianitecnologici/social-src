# MARRtino Python program #

MARRtino Python programming with basic actions.

## Install ##

Download the following packages in your catkin workspace and compile them with catkin_make:

* https://gitlab.com/srrg-software/srrg_cmake_modules
* https://gitlab.com/srrg-software/srrg_core
* https://gitlab.com/srrg-software/srrg_core_ros
* https://gitlab.com/srrg-software/srrg2_orazio_core
* https://gitlab.com/srrg-software/srrg2_orazio_ros


## Program ##

* Write your Python program (see robot_program_1.py as an example).

```
from robot_cmd_ros import *

begin()

<your program>

end()
```


Some available commands (implemented in robot_cmd_ros.py):

```
begin()
end()
stop()
forward(r=1)
backward(r=1)
left(r=1)
right(r=1)
wait(r=1)
bip(r=1)
bop(r=1)
```


## Run ##

* Start the robot

Real MARRtino
```
$ cd <..>/marrtino_apps/robot/
$ roslaunch robot.launch

```

Simulator
```
$ cd <..>/marrtino_apps/stage/
$ roslaunch simrobot.launch
```


* Run your program

```
$ cd <..>/marrtino_apps/program
$ python <your_program>.py
```


## Client/Server ##

To run a program from a remote machine, use the client server mode.

* Run the server (on the robot machine)

```
$ ./robot_program_server.py <PORT>
```

* Send a Python program from a client (see robot_program_client.py for example).

```
$ ./robot_program_client.py <HOST> <PORT>
```

## Audio ##

* Run the AudioServer (see audio app) to play sounds

* To add new sounds, add a WAV file in the audio app directory (see the README file in audio app)
and add a command in robot_cmd.py (similarly to bip and bop functions).

## Old version ##


Programming the robot using ```srrg_orazio_core``` and ```marrtino_programming``` (i.e., without ROS) was supported with until commit

```
commit 1a7cffe3fada05390c74d07b62244df7a484352a
Date:   Wed Dec 27 12:12:31 2017 +0100
```

