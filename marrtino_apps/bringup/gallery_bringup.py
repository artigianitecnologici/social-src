#!/usr/bin/env python

from __future__ import print_function

import _thread
import socket

import argparse

import sys, time, os, glob, shutil, math, datetime

from tmuxsend import TmuxSend

def getCameraResolution():
    width=640
    height=480
    camres = os.getenv("CAMRES")
    print(camres)
    if camres!=None and camres!='' and camres!='None':
        (width, height) = eval(camres)
    return (width, height)

def getFramerate():
    framerate = 10
    framerate = os.getenv("CAMFRAMERATE")
    print(framerate)
    #if framerate!=None and framerate!='' and framerate!='None':
    return (framerate)

def getDevice():
    camdevice = '/dev/video0'
    camdevice = os.getenv("CAMDEVICE")
    print(camdevice)
    #if framerate!=None and framerate!='' and framerate!='None':
    return (camdevice)

def run_server(port):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.settimeout(3)
    # Bind the socket to the port
    server_address = ('', port)
    sock.bind(server_address)
    sock.listen(1)

    print("Vision server started on port %d ..." %port)

    tmux = TmuxSend('bringup', ['shot','gallery','free','cmd','cmd2'])

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
                cfolder = os.getenv('MARRTINO_APPS_HOME')+"/gallery"
                
                if data==b'@shotnode':  
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'python3 shot_node.py ')
                elif data==b'@shotnodekill':
                    tmux.Cc(0)
                    
                elif data==b'@startrobot':
                    tmux.cmd(2,'cd %s' %cfolder)
                    tmux.cmd(2,'roslaunch robot.launch')

                elif data==b'@gallery':
                    tmux.cmd(1,'cd %s' %cfolder)
                    tmux.cmd(1,'python3 app.py . -l 0.0.0.0')
                elif data==b'@gallerykill':
                    tmux.Cc(1)
                             
                else:
                    print('Unknown command %s' %data)



if __name__ == '__main__':

    default_port = 9253

    parser = argparse.ArgumentParser(description='gallery bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)

