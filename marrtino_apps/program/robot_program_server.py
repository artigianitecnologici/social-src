#!/usr/bin/env python

import sys
import os
import socket
import importlib
import re
#import robot_cmd_ros

TCP_IP = ''
TCP_PORT = 5000
BUFFER_SIZE = 20000


def start_server():
    global TCP_IP
    global TCP_PORT
    global BUFFER_SIZE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(1)

    #cmd = "play --no-show-progress --null -c2 synth sin gain -100 &"
    #os.system(cmd)

    run=True

    while run:
        print "Robot Program Server: waiting for connections on port", TCP_PORT
        try:
            conn, addr = s.accept()
        except KeyboardInterrupt:
            print("  User quit")
            sys.exit(0)
        print "Connection address:", addr
        connected = True
        while connected:
            try:
                data = conn.recv(BUFFER_SIZE)
            except:
                print "Connection closed."
                break
            if not data:
                break
            print "Received: ",data
            conn.send("OK\n")

            if (data=='stop'):
                print('Stop code and robot')
                robot_stop_request()
            else:
                print('Run code')
                data = 'from robot_cmd_ros import *\n\n'+data
                try:
                    exec(data)
                except Exception as e:
                    print("CODE EXECUTION ERROR")
                    print e

	    conn.close()
	    print "Closed connection"




if __name__ == "__main__":

    if (len(sys.argv)==2):
	    TCP_PORT = int(sys.argv[1])
    elif (len(sys.argv)==3):
	    TCP_PORT = int(sys.argv[2])
	    if (sys.argv[1]=="-norobot"):
		    robot_cmd.userobot = False
    #else:
	#    print "Use: robot_program_server [-norobot] <TCP_port>"
	#    sys.exit(1)

    start_server()

