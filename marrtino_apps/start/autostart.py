#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time
try:
    import yaml
except Exception as e:
    print(e)
    print("Try install yaml with    sudo apt-get install python3-yaml")
    sys.exit(1)

import subprocess
import re


def find_webcam_by_name(device_name):
    # Run v4l2-ctl to list video devices
    result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
    video_devices = result.stdout

    # Use regex to find the device with the specified name
    pattern = re.compile(rf'{re.escape(device_name)}:.*?(/dev/video\d+)', re.DOTALL)
    match = pattern.search(video_devices)

    # Check if the webcam information is found
    if match:
        # Extract the video device path
        video_device_path = match.group(1)
        
        print("Found Webcam Information:")
        print(video_devices)

        print(f"Associated {video_device_path}")
        return video_device_path
    else:
        print(f"Webcam with device name '{device_name}' not found.")

def readconfig(yamlfile):
    info = {}
    with open(yamlfile, 'r') as f:
        info = yaml.safe_load(f)
    return info


def systemcmd(cmdkey, port):
    cmd = "echo '%s' | netcat -w 1 localhost %d" %(cmdkey,port)
    print("  "+cmd)
    os.system(cmd)
    time.sleep(3)
    

def getconfig(section,key):
    try:
        r = config[section][key]
    except:
        #print("No value for %s:%s" %(section,key))
        r = None
    return r

def autostart(config, dostart):
    print("auto start:")

    #  simulator
    if getconfig('simulator','stage'):
        mapname = getconfig('simulator','mapname')
        mapdir = getconfig('simulator','mapdir')
        robottype = getconfig('simulator','robottype')
        nrobots = getconfig('simulator','nrobots')
        if mapdir!='default':
            print("TODO: set mapdir to %s !!!" %mapdir)
        simtime = 'rosparam set /use_sim_time '
        simtimeval = 'true' if dostart else 'false'
        simtime = simtime + simtimeval
        cmd = 'docker exec -it base bash -ci "%s"' %simtime
        os.system(cmd)
        cmd = "%s;%s;%d" %(mapname,robottype,nrobots) if dostart else "@stagekill"
        systemcmd(cmd,9235)

    # devices
    if getconfig('devices','robot'):
        cmd = '@robot' if dostart else '@robotkill'
        systemcmd(cmd,9236)
    if getconfig('devices','joystick') == '2wd':
        cmd = '@joystick' if dostart else '@joystickkill'
        systemcmd(cmd,9240)
    if getconfig('devices','joystick') == 'keyboard':
        cmd = '@keyboard' if dostart else '@joystickkill'
        systemcmd(cmd,9240)
    elif getconfig('devices','joystick') == '4wd':
        cmd = '@joystick4wd' if dostart else '@joystickkill'
        systemcmd(cmd,9240)
    cam = getconfig('devices','camera') 
    if cam=='usbcam' or cam=='astra' or cam=='xtion':
        cmd = '@%s' %cam if dostart else '@camerakill'
        systemcmd(cmd,9237)
    else :
        device_name_to_find = "USB 2.0 Camera"
        # Find and print information about the webcam
        device_name = find_webcam_by_name(device_name_to_find)
        cmd = '@camera_' + device_name
        print(cmd)
        systemcmd(cmd,9237)

    #if cam=='shot':
    #    cmd = '@%s' %cam if dostart else '@camerakill'
    #    systemcmd(cmd,9253)
    #if cam=='d345' :
    #    cmd = '@%s' %cam if dostart else '@camerakill'
    #    systemcmd(cmd,9237)  
    las = getconfig('devices','laser')
    if  las=='hokuyo' or las=='rplidar' or las=='ld06':
        cmd = '@%s' %las if dostart else '@laserkill'
        systemcmd(cmd,9238)


    # functions
    if getconfig('functions','localization'):
        cmd = '@loc' if dostart else '@lockill'
        systemcmd(cmd,9238)
    if getconfig('functions','navigation') == 'gbn':
        cmd = '@gbn' if dostart else '@gbnkill'
        systemcmd(cmd,9238)
    elif getconfig('functions','navigation') == 'move_base':
        cmd = '@movebase' if dostart else '@movebasekill'
        systemcmd(cmd,9238)
    elif getconfig('functions','navigation') == 'move_base_gbn':
        cmd = '@movebasegbn' if dostart else '@movebasekill'
        systemcmd(cmd,9238)
    if getconfig('functions','navigation_rviz'):
        cmd = '@rviz' if dostart else '@rvizkill'
        systemcmd(cmd,9238)
    if getconfig('functions','mapping') == 'gmapping':
        cmd = '@gmapping' if dostart else '@gmappingkill'
        systemcmd(cmd,9241)
    elif getconfig('functions','mapping') == 'srrg_mapper':
        cmd = '@srrgmapper' if dostart else '@srrgmapperkill'
        systemcmd(cmd,9241)
    if getconfig('functions','mapping_rviz'):
        cmd = '@rviz' if dostart else '@rvizkill'
        systemcmd(cmd,9241)

    if getconfig('functions','videoserver'):
        cmd = '@videoserver' if dostart else '@videoserverkill'
        systemcmd(cmd,9237)
    if getconfig('functions','rosbridge'):
        cmd = '@rosbridge' if dostart else '@rosbridgekill'
        systemcmd(cmd,9237)
    if getconfig('functions','gallery'):
        cmd = '@gallery' if dostart else '@gallerykill'
        systemcmd(cmd,9253)
        cmd = '@shotnode' if dostart else '@shotnodekill'
        systemcmd(cmd,9253)
    if getconfig('functions','apriltags'):
        cmd = '@apriltags' if dostart else '@apriltagskill'
        systemcmd(cmd,9237)
    if getconfig('functions','objrec'):
        cmd = '@objrec' if dostart else '@objreckill'
        systemcmd(cmd,9242)
    if getconfig('functions','audioserver'):
        cmd = '@audio' if dostart else '@audiokill'
        systemcmd(cmd,9239)
    soc = getconfig('functions','social')
    if soc=='on':
        soc='social'
    if soc=='social':
        cmd = '@robotsocial' if dostart else '@socialkill'
        systemcmd(cmd,9250)
    elif soc=='notracker':
        cmd = '@socialnotracker' if dostart else '@socialkill'
        systemcmd(cmd,9250)
    elif soc=='noservo':
        cmd = '@socialnoservo' if dostart else '@socialkill'  
        systemcmd(cmd,9250)

    if getconfig('functions','pantilt'):
        cmd = '@pantilt_start' if dostart else '@pantilt_kill'
        systemcmd(cmd,9249)

#

# Use python autostart.py [start.yaml file] [--kill]

if __name__=='__main__':

    autostartfile = "autostart.yaml"
    yamlfile = os.getenv('MARRTINO_APPS_HOME')+"/"+autostartfile
    dostart = True

    if len(sys.argv)>1 and sys.argv[1]=='--kill':
        dostart = False
    if len(sys.argv)>2 and sys.argv[2]=='--kill':
        dostart = False
    if len(sys.argv)>1 and sys.argv[1][0]!='-':
        yamlfile = sys.argv[1]


    
    if not os.path.isfile(yamlfile):
        yamlfile = os.getenv('HOME')+"/"+autostartfile
    if not os.path.isfile(yamlfile):
        print("File %s not found!!!" %autostartfile)
        sys.exit(1) 

    config = readconfig(yamlfile)
    autostart(config, dostart)


