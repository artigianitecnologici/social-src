#!/usr/bin/env python

from __future__ import print_function

import thread
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

    tmux = TmuxSend('bringup', ['camera','vidserver','april','takephoto','cmd','rosbridge'])

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
                cfolder = os.getenv('MARRTINO_APPS_HOME')+"/camera"
                mfolder = os.getenv('MARRTINO_APPS_HOME')+"/marker"
                if data=='@usbcam':
                    r = getCameraResolution()
                    
                    imsz = ''
                    if r != None:
                        imsz = 'image_width:=%d image_height:=%d' %(r[0],r[1])
                        print("Camera resolution: %s" %(str(r)))
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'roslaunch usbcam.launch '+imsz)
                elif data[0:8]=='@usbcam_':  # @usbcam_<width>_<height>
                    v = data.split("_")
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'roslaunch usbcam.launch ' + 'image_width:=%d image_height:=%d framerate:=%s ' %(int(v[1]),int(v[2])))
                elif data[0:8]=='@camera_' or data[0:7]=='camera_' :  # @camera_/dev/video2
                    v = data.split("_")
                    tmux.cmd(0,'cd %s' %cfolder)
                    mycmd = 'roslaunch usbcam.launch '+ 'image_width:=640 image_height:=480 device:=' + v[1]
                    print(mycmd)
                    tmux.cmd(0,mycmd)

                elif data=='@astra':
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'roslaunch astra.launch')
                elif data=='@xtion':
                    tmux.cmd(0,'cd %s' %cfolder)
                    tmux.cmd(0,'roslaunch xtion2.launch')
                elif data=='@camerakill':
                    tmux.Cc(0)
                elif data=='@videoserver':
                    tmux.cmd(1,'cd %s' %cfolder)
                    tmux.cmd(1,'roslaunch videoserver.launch')
                elif data=='@videoserverkill':
                    tmux.Cc(1)
                elif data=='@rosbridge':
                    tmux.cmd(5,'cd %s' %cfolder)
                    tmux.cmd(5,'roslaunch rosbridge.launch')
                elif data=='@rosbridgekill':
                    tmux.Cc(1)
                elif data=='@apriltags':
                    tmux.cmd(2,'cd %s' %mfolder)
                    tmux.cmd(2,'roslaunch tags.launch')
                elif data=='@apriltagskill':
                    tmux.Cc(2)
                elif data=='@takephoto':
                    tmux.cmd(3,'cd %s' %cfolder)
                    tmux.cmd(3,'python takephoto.py')
                elif data=='@takephotokill':
                    tmux.Cc(3)
                else:
                    print('Unknown- command %s' %data)
                    print(data[0:8])
            

if __name__ == '__main__':

    default_port = 9237

    parser = argparse.ArgumentParser(description='vision bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)
