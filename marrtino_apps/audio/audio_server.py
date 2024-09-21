
# Only PCM 16 bit wav 44100 Hz - Use audacity or sox to convert audio files.

# WAV generation

# Synth
# sox -n --no-show-progress -G --channels 1 -r 44100 -b 16 -t wav bip.wav synth 0.25 sine 800 
# sox -n --no-show-progress -G --channels 1 -r 44100 -b 16 -t wav bop.wav synth 0.25 sine 400 

# Voices
# pico2wave -l "it-IT" -w start.wav "Bene! Si Parte!"
# Then convert wav files to to 44100 Hz

# Note: some initial sound may not be played.

# alsaaudio examples
# https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html

import threading
import time
import socket
import sys, os, platform
import re
import wave
import argparse

import rospy
import std_msgs.msg

use_sound_play = False
use_alsaaudio = True


try:
    from sound_play.msg import SoundRequest
    from sound_play.libsoundplay import SoundClient
except:
    print('ROS package sound_play required.')
    print('Install with: sudo apt-get install ros-kinetic-audio-common libasound2')
    use_sound_play = False
    #sys.exit(0)


try:
    import sox
except:
    print('sox required. Install with:   pip install --user sox')
    sys.exit(0)


try:
    import alsaaudio
except:
    print('alsaaudio required. Install with:   pip install --user pyalsaaudio')
    use_alsaaudio = False
    #sys.exit(0)



from asr_server import ASRServer



SOUNDS_DIR = "sounds/"  # dir with sounds
soundfile = None        # sound file

# SPEECH_TOPIC = "/speech/to_speak"
# SPEECHSTATUS_TOPIC = "/speech/status"



tts_server = None
asr_server = None

# def speak_callback(data):
#     global tts_server
#     if tts_server is not None:
#         # print(data.data)
#         full_string = data.data.split("###")
#         if len(full_string) > 1:
#             data.data = full_string[0]
#             language = full_string[1]
#         else:
#             language = "it"
#         rospy.loginfo(rospy.get_caller_id() + "%s %s" %(SPEECH_TOPIC,data.data))
#         tts_server.say(data.data, language)
        
# ROS node with speech topic subscriber
rospy.init_node('audioserver') #, disable_signals=True)
# rospy.Subscriber(SPEECH_TOPIC,std_msgs.msg.String,speak_callback)
# status_pub =rospy.Publisher(SPEECHSTATUS_TOPIC, std_msgs.msg.String, queue_size=10)

# def SpeechStatus(msg):
#     status_pub.publish(msg)




def TTS_callback(in_data, frame_count, time_info, status):
    global soundfile
    if (soundfile==None):
        return (None, True)
    else:
        data = soundfile.readframes(frame_count)
        return (data, pyaudio.paContinue)


class TTSServer(threading.Thread):    

    def __init__(self, port, output_device):
        global use_alsaaudio, use_sound_play
        global speechstatus_pub
        threading.Thread.__init__(self)

        # Initialize audio player
        self.streaming = False
        self.output_device = output_device
        self.soundhandle = None
        

        m = platform.machine()
        print ("Machine type:" , m)
        if (m[0:3]=='arm'):
            use_sound_play = False

        if (use_sound_play):
            os.system('roslaunch sound_play.launch &')
            time.sleep(5)
            #rospy.init_node('sound_client', disable_signals=True)
            use_alsaaudio = False
        elif (use_alsaaudio):
            self.init_alsaaudio()
        else:
            print('Cannot initialize audio interface')

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(3)
        # Bind the socket to the port
        server_address = ('', port)
        self.sock.bind(server_address)
        self.sock.listen(1)
        print("TTS Server running on port %d ..." %port)
        
        self.dorun = True
        self.connection = None

        # Dictionary of sounds
        self.Sounds = {}
        self.Sounds['bip'] = wave.open(SOUNDS_DIR+'bip.wav', 'rb') 
        self.idcache = 0
    

    def init_alsaaudio(self):
        print("Audio devices available")
        pp = alsaaudio.pcms()
        if (self.output_device=='sysdefault'):
            # select proper sysdefault name
            for l in pp:
                print('  %s' %l)
                if (l[0:7]=='default'):
                    print("choose ",l)
                    self.output_device = l # choose default device
                    break
        print("Audio device used: %s" %self.output_device)

        self.aa_stream = None
        retry = 3
        while retry>0:
            try:
                self.aa_stream = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL, self.output_device)
                retry = 0
            except Exception as e:
                print(e)
                retry -= 1
                time.sleep(2)

        if self.aa_stream == None:
            retry = 3
            while retry>0:
                try:
                    self.output_device='default'
                    print("Audio device used: %s" %self.output_device)
                    self.aa_stream = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL, self.output_device)
                    retry = 0
                except Exception as e:
                    print(e)
                    retry -= 1
                    time.sleep(2)

        self.audio_rate = 44100
        self.periodsize = 5512 # self.audio_rate / 8

        if self.aa_stream != None:
            self.aa_stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.aa_stream.setchannels(1)
            self.aa_stream.setrate(self.audio_rate)
            self.aa_stream.setperiodsize(self.periodsize)



    def stop(self):
        self.dorun = False
        

    def connect(self):
        connected = False
        while (self.dorun and not connected):
            try:
                # print('Waiting for a connection ...')
                # Wait for a connection
                self.connection, client_address = self.sock.accept()  # blocking
                self.connection.settimeout(3) # timeout when listening (exit with CTRL+C)
                connected = True
                print('TTS Server Connection from %r' %client_address)
            except:
                pass #print("Listen again ...")


    def reply(self,mstr):
        if (self.connection != None):
            try:
                mstr = mstr.encode('utf-8')
                self.connection.send(mstr+'\n\r')
            except:
                print('Connection closed')


    def setVolume(self,volperc): # volume in percentag [0-100]
        cmdstr = 'amixer set PCM %d%%' %volperc
        os.system(cmdstr)

    def connection_run(self):
        self.connect()  # blocking
        try:
            # Receive the data in small chunks
            while (self.dorun):
                try:
                    data = self.connection.recv(320)
                    data = data.strip()
                except socket.timeout:
                    data = "***"
                except:
                    data = None

                if (data!=None and data !="" and data!="***"):
                    if data!="ASR":
                        print ('TTS Received [%s]' % data)
                    if (data.startswith('TTS')):
                        lang = 'en-US' # default language
                        strsay = data[4:]
                        if (data[3]=='['):
                            vd = re.split('\[|\]',data)
                            lang = vd[1]
                            strsay = vd[2]
                        self.say(strsay,lang)
                        self.reply('OK')

                    elif (data=="ASR"):
                        #print('asr request')
                        bh = asr_server.get_asr()
                        self.reply(bh)
                        if bh!='':
                            print('ASR sent [%s]' %bh)

                    elif (data.startswith('SOUND')):
                        self.play(data[6:]) # play this sound
                        self.reply('OK')
                    #print 'sending data back to the client'
                    #self.connection.sendall("OK")
                    else:
                        print('Message not understood: %s' %data)
                        self.reply('ERR')
                elif (data == None or data==""):
                    break
        finally:
            print ('TTS Server Connection closed.')
            # Clean up the connection
            if (self.connection != None):
                self.connection.close()
                self.connection = None


    def run(self):
        global asr_server

        if (use_sound_play and self.soundhandle == None):
            self.soundhandle = SoundClient()
            time.sleep(3)

        self.setVolume(99)  # set volume (99% = +3 dB)

        #print('bip')
        #self.play('bip')
        #time.sleep(3)

        self.say('Hello!', 'en')
        self.say('Audio server is running.', 'en')
        time.sleep(3)

        while (self.dorun):
            self.connection_run()

        self.say('Audio server has been closed.', 'en')
        time.sleep(2)
        self.aa_stream = None

   

    def say(self, data, lang):
        print('Say %r' %data)
        
        SpeechStatus('START')

        if (use_sound_play):
            voice = 'voice_kal_diphone'
            volume = 1.0
            print ('Saying: %s' % data)
            print ('Voice: %s' % voice)
            print ('Volume: %s' % volume)
            
            self.soundhandle.say(data, voice, volume)
            rospy.sleep(3)

        elif (use_alsaaudio):
            cachefile = 'cache'+str(self.idcache)
            self.idcache = (self.idcache+1)%10
            tmpfile = "/tmp/cache.wav"
            ofile = "%s%s.wav" %(SOUNDS_DIR, cachefile)
            cmd = 'rm %s %s' %(tmpfile, ofile)
            os.system(cmd)
            if (lang=='en'):
                lang = 'en-US'
            elif (len(lang)==2):
                lang = lang+'-'+lang.upper()
            time.sleep(0.2)
            cmd = 'pico2wave -l "%s" -w %s " , %s"' %(lang,tmpfile, data)
            print(cmd)
            os.system(cmd)
            time.sleep(0.2)

            # convert samplerate
            tfm = sox.Transformer()
            tfm.rate(samplerate=self.audio_rate)
            tfm.build(tmpfile, ofile)
            time.sleep(0.2)

            self.play(cachefile)
            SpeechStatus('STOP')
        else:
            print('Cannot play audio. No infrastructure available.')


    def play(self, name):
        if (use_alsaaudio):
            print('Playing %s ...' %name)
            soundfile = None
            i = 0    
            while (i<3): #((not name in self.Sounds) and (i<3)):
                try:
                    soundfile = wave.open(SOUNDS_DIR+name+".wav", 'rb')
                    #self.Sounds[name] = soundfile
                except:
                    print ("File %s%s.wav not found." %(SOUNDS_DIR,name))
                    time.sleep(1)
                i += 1
            
            if (soundfile != None and use_alsaaudio): #(name in self.Sounds):
                self.playwav_aa(soundfile)
            print('Play completed.')


    def playwav_aa(self, soundfile):
        soundfile.setpos(0)
        data = soundfile.readframes(self.periodsize)
        while (len(data)>0):
            # print('stream data %d' %(len(data)))
            if self.aa_stream != None:
                self.aa_stream.write(data)  
            data = soundfile.readframes(self.periodsize)  
 

#    def playwav_pa(self, sfile):
#        global soundfile
#        self.streaming = True
#        self.stream = self.pa.open(format = 8, #self.pa.get_format_from_width(f.getsampwidth#()),  
#                channels = 1, #f.getnchannels(),  
#                rate = 44100, #f.getframerate(),  
#                output = True,
#                stream_callback = TTS_callback,
#                output_device_index = self.output_device)
#        soundfile = sfile
#        soundfile.setpos(0)
#        self.stream.start_stream()
#        while self.stream.is_active():
#            time.sleep(1.0)
#        self.stream.stop_stream()  
#        self.stream.close()  
#        self.streaming = False




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='audio_server')
    parser.add_argument('-ttsport', type=int, help='TTS server port [default: 9001]', default=9001)
    parser.add_argument('-asrport', type=int, help='ASR server port [default: 9002]', default=9002)
    parser.add_argument('-device', type=str, help='audio device [default: \'sysdefault\']', default='sysdefault')

    args = parser.parse_args()

    tts_server = TTSServer(args.ttsport,args.device)
    asr_server = ASRServer(args.asrport)

    tts_server.start()
    time.sleep(1)
    asr_server.start()
    
    
    
    

    print("audioserver listening to topic %s" %SPEECH_TOPIC)

    run = True
    while (run and not rospy.is_shutdown()):
        try:
            rospy.sleep(3)
            #if (not tts_server.streaming):
            #    cmd = 'play -n --no-show-progress -r 44100 -c1 synth 0.1 sine 50 vol 0.01' # keep sound alive
            #    os.system(cmd)
        except KeyboardInterrupt:
            print ("Exit")
            run = False

    tts_server.stop()
    asr_server.stop()
    sys.exit(0)


