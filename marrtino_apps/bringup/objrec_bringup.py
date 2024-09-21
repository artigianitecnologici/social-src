#!/usr/bin/env python

from __future__ import print_function

try:
  import thread
except:
  import threading

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
    print("MARRtino object recognition server started on port %d ..." %port)

    tmux = TmuxSend('bringup', ['objrec','cmd'])

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
                data = data.decode('utf-8')
                print(data)
                vfolder = os.getenv('MARRTINO_APPS_HOME')+"/vision"
                if data=='@objrec':
                    tmux.cmd(0,'cd %s' %vfolder)
                    tmux.cmd(0,'python mobilenet_objrec.py --server')
                elif data=='@objreckill':
                    tmux.Cc(0)

                else:
                    print('Unknown command %s' %data)


if __name__ == '__main__':

    default_port = 9242

    parser = argparse.ArgumentParser(description='objrec bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)

