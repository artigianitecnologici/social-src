#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from gtts import gTTS
import os
import socket
import subprocess

class TTSNode:

    def __init__(self):
        rospy.init_node('tts_node', anonymous=True)
        rospy.loginfo('Start tts_node')
        
        self.publisher_ = rospy.Publisher('/speech/status', String, queue_size=10)
        self.subscriber_ = rospy.Subscriber('/speech/to_speak', String, self.tts_callback)
        
        self.finished_speaking = False
        self.loop_count_down = 0
        self.LOOP_FREQUENCY = 10  # Example loop frequency if needed

    def tts_callback(self, msg):
        text = msg.data
        rospy.loginfo('Received text: "%s"' % text)
        self.finished_speaking = False
        self.loop_count_down = 0

        # Check internet connectivity
        if self.is_connected():
            # Convert text to speech
            tts = gTTS(text, lang='it')
            tts.save('output.mp3')
            os.system('mpg321 output.mp3')
            # Publish the fact that the TTS is done
            self.publisher_.publish(String(data='TTS done'))
        else:
            # rospy.logerr('No internet connection')
            filename = "/tmp/robot_speach.wav"
            # create wav file using pico2wav from adjusted text.
            cmd = ['pico2wave', '--wave=' + filename, '--lang=' + 'it-IT', text]
            subprocess.call(cmd)
            # Play created wav file using sox play
            cmd = ['play', filename, '--norm', '-q']
            subprocess.call(cmd)
            # Set up to send talking finished
            self.finished_speaking = True
            self.loop_count_down = int(self.LOOP_FREQUENCY * 2)

    def speaking_finished(self):
        if self.finished_speaking:
            self.loop_count_down -= 1
            if self.loop_count_down <= 0:
                rospy.logerr('speaking finished')
                self.finished_speaking = False
                self.publisher_.publish(String(data='TTS done'))

    def is_connected(self):
        try:
            # Try to connect to a well-known website
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False

def main():
    tts_node = TTSNode()

    # Keep node running until it is shut down
    rospy.spin()

if __name__ == '__main__':
    main()
