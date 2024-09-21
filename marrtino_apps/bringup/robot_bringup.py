#!/usr/bin/env python

from __future__ import print_function

import thread
import socket
 
import argparse

import sys, time, os, glob, shutil, math, datetime

from tmuxsend import TmuxSend


def run_server(port):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.settimeout(3)
    # Bind the socket to the port
    server_address = ('', port)
    sock.bind(server_address)
    sock.listen(1)
    print("ROS navigation server started on port %d ..." %port)

    tmux = TmuxSend('bringup', ['robot','cmd'])

    connected = False
    dorun = True
    while dorun:

        if not connected:
            print("-- Waiting for connection ...")
        while (dorun and not connected):
            try:
                # Wait for a connection
                connection, client_address = sock.accept()
                connected = True
                print ('-- Connection from %s'  %client_address[0])
            except KeyboardInterrupt:
                print("User interrupt (quit)")
                dorun = False
            except Exception as e:
                print(e)
                pass # keep listening
    
        if not dorun:
            return

        # print("-- Waiting for data...")
        data = None
        while dorun and connected and data is None:
            # receive data
            try:
                #connection.settimeout(3) # timeout when listening (exit with CTRL+C)
                data = connection.recv(320)  # blocking
                data = data.strip()
            except KeyboardInterrupt:
                print("User interrupt (quit)")
                dorun = False
            except socket.timeout:
                data = None
                print("socket timeout")

        if data is not None:
            if len(data)==0:
                connected = False
            else:
                print(data)
                rfolder = os.getenv('MARRTINO_APPS_HOME')+"/robot"
                cfolder = os.getenv('MARRTINO_APPS_HOME')+"/config"
                if data=='@robot':
                    tmux.cmd(0,'cd %s' %rfolder)
                    tmux.cmd(0,'roslaunch robot.launch')
                elif data=='@robotkill':
                    tmux.Cc(0)
                elif data=='@orazioweb':
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'./run_orazio2_web.bash')
                elif data=='@orazio2018web':
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'./run_orazio_web.bash')
                elif data=='@oraziowebkill':
                    tmux.Cc(0)
                elif data=='@firmware':
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'./uploadfirmware.bash')
                elif data[0:15]=='@firmwareparams':
                    # firmwareparams;[arduino|ln298|pka03|marrtino2019]
                    v = data.split(";")
                    mb = 'marrtino2019'
                    if len(v)>1:
                        mb = v[1]
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'./uploadfirmwareparams.bash %s' %mb)
                else:
                    print('Unknown command %s')



if __name__ == '__main__':

    default_port = 9236

    parser = argparse.ArgumentParser(description='robot bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)

