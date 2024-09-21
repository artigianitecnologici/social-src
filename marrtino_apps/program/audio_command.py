#!/usr/bin/env python

from robot_cmd_ros import *

begin()

bip()

wait()

run = True

while run:

    a = asr();
    if (a!=''):
        print a

    if ('avanti' in a):
        forward();
    elif ('dietro' in a):
        backward();
    elif ('sinistra' in a):
        left();
    elif ('destra' in a):
        right();
    elif ('esci' in a):
        run = False;
    elif (a!=''):
        bop()

    wait()

end()

