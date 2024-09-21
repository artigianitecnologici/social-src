import os, datetime

URLbase = 'http://www.diag.uniroma1.it/~iocchi/marrtino/'
updatesfile = 'updates.txt'


def getversion(upstr):
    r = ''
    if ('marrtino_update' in upstr):
        vstr = upstr.split('_')
        l = len(vstr[2])
        r = vstr[2][1:l-5]
    return r


# cd ~/install'
os.chdir(os.getenv('HOME')+'/install')
os.system('mkdir -p .log')

ever = os.getenv('MARRTINO_VERSION')

fmv = open(os.getenv('HOME')+'/.marrtino_version')
fver = fmv.read().strip()
fmv.close()

if (ever>fver):
    cver = ever
else:
    cver = fver

print("Current version: %s" %cver)

if cver[0]=='4':
    print("MARRtino system version 4 detected.")
    updatesfile = 'updates4.txt'


cmd = 'wget -N '+URLbase+updatesfile
os.system(cmd)

upfile = open(updatesfile,"r")
lines = upfile.readlines()
vmax = ''
for l in lines:
    v = getversion(l.strip())
    if (v>cver):    
        print('New version available: %s' %v)
        if (vmax==''):
            vmax=v
upfile.close()

tm = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

logfile = os.getenv('HOME')+"/install/.log/install_%s.log" %tm

if (vmax!=''):
    val = raw_input('Install version %s? [y/n] ' %(vmax))

    if (str(val)=='y' or str(val)=='Y'):
        print("Installing marrtino v%s ..." %(vmax))
        upcmd = 'marrtino_update_v%s.bash' %(vmax)
        cmd = 'wget -N '+URLbase+upcmd
        print(cmd)
        os.system(cmd)
        cmd = 'chmod a+x '+upcmd
        print(cmd)
        os.system(cmd)
        cmd = './'+upcmd
        print(cmd)
        print('See installation output on another terminal with command:')
        print('tail -f '+logfile)
        print('\nInstallation in progress... please wait...\n')
        os.system(cmd + " >%s 2>&1 " %logfile)
        print('Installation completed.\n')
        os.system('tail '+logfile)
        print('\n')
else:
    print('MARRtino system %s is currently updated to the last version.' %cver)



