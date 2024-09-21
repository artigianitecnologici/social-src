#!/usr/bin/env python

'''
Copyright (c) 2016, Nadya Ampilogova
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

* Revised Luca Iocchi 2019-2021
'''


from __future__ import print_function
import os,sys,socket
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import argparse
import numpy

ROS_NODE_NAME = 'takephoto'
TAKEPHOTO_TOPIC = '/takephoto'
PARAM_takephoto_image_folder = '%s/imagefolder' %ROS_NODE_NAME
PARAM_result = '%s/imageresult' %ROS_NODE_NAME

# select topic of type sensor_msgs/Image
def autoImageTopic():
    topics = rospy.get_published_topics()
    for t in topics:
        if t[1]=='sensor_msgs/Image' and 'depth' not in t[0] and '/ir/' not in t[0] and 'image_rect' not in t[0]:
            return t[0]
    return None


class TakePhoto:

    def __init__(self, img_topic=None, takephoto_topic=None):

        self.bridge = CvBridge()
        self.image_received = False
        self.image = None # last image received

        if img_topic is None:
            img_topic = autoImageTopic()

        if img_topic is None:
            rospy.logerr("Cannot find any image topic!!! Aborting.")
            sys.exit(0)

        rospy.loginfo("Image topic: %s" %img_topic)
        self.image_sub = rospy.Subscriber(img_topic, Image, self.image_cb)

        # Allow up to one second to connection
        rospy.sleep(1)

        if takephoto_topic!=None:
            rospy.loginfo("TakePhoto topic: %s" %takephoto_topic)
            rospy.Subscriber(takephoto_topic, String, self.take_photo_cb)

        # Folder for saving images
        self.takephoto_image_folder = '.'

        if (rospy.has_param(PARAM_takephoto_image_folder)):
            self.takephoto_image_folder = rospy.get_param(PARAM_takephoto_image_folder)

        print("Save image folder: %s" %self.takephoto_image_folder)

        self.sendimage_server = 'localhost'
        self.sendimage_port = 9250

        print("Default send image server: %s:%d"
               %(self.sendimage_server,self.sendimage_port) )



    def image_cb(self, data):
        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        self.image_received = True
        self.image = cv_image

    def take_image(self, img_title, usetimestamp=False):
        if self.image_received:
            # Get save folder
            if (rospy.has_param(PARAM_takephoto_image_folder)):
                self.takephoto_image_folder = rospy.get_param(PARAM_takephoto_image_folder)
            # Set filename
            timestr = ""
            if usetimestamp:
                timestr = time.strftime("%Y%m%d-%H%M%S-")
            img_file = self.takephoto_image_folder + "/" + timestr + img_title
            # Save an image
            rospy.loginfo("Saving image " + img_file)
            cv2.imwrite(img_file, self.image)
            cmd = 'ln -sf %s %s/lastimage.%s' \
                    %(img_file,self.takephoto_image_folder,img_title[-3:])
            os.system(cmd)
            rospy.loginfo("Saved image " + img_file)
            return True
        else:
            rospy.loginfo("No images received")
            return False

    def send_image(self, width, height):
        if self.image_received:
            
            sendimage = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            sendimage = cv2.resize(sendimage, (width,height))

            data = numpy.array(sendimage)
            stringData = data.tostring()

            try:
                rospy.set_param(PARAM_result, '')
                sock = socket.socket()   # connection to server
                sock.connect((self.sendimage_server, self.sendimage_port))
                (h,w,c) = sendimage.shape
                print("Sending %dx%d image " %(w,h))
                sock.sendall("RGB %d %d\n\r" %(w,h))
                rospy.sleep(0.2)
                sock.sendall(stringData);
                data = sock.recv(256)
                data = data.strip().decode('UTF-8')
                print(data)
                rospy.set_param(PARAM_result, data)
                sock.close()
            except Exception as e:
                print(e)
                print("Cannot send image to %s:%d" %(self.sendimage_server, self.sendimage_port))

    def show_image(self):
        if self.image_received:
            cv2.imshow('image',self.image)
            cv2.waitKey(3000)

    def take_photo_cb(self, msg):
        print("takephoto: received msg: %s" %msg.data)
        if msg.data == "get":
            # Take a photo
            self.take_image('photo.jpg', usetimestamp=True)
        elif msg.data[0:4] == "send":
            v = msg.data.split(" ")
            if (len(v)>=3):
                self.sendimage_server = v[1]
                self.sendimage_port = int(v[2])
            w=224
            h=224
            if (len(v)>=5):
                w = int(v[3])
                h = int(v[4])
            # Take a photo
            self.send_image(w,h)

    def waitForImage(self):
        time.sleep(0.5)
        while not self.image_received:
            time.sleep(0.5)



def take_image():
    rospy.init_node(ROS_NODE_NAME, anonymous=False)
    camera = TakePhoto()
    camera.waitForImage()
    img = camera.image
    return img

# To use it from a local machine (other than the one running the camera node)
# export ROS_IP=`hostname -I`
# export ROS_MASTER_URI=http://10.3.1.1:11311

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-image_topic", type=str, default=None,
                        help="Image topic (default: auto detect)")
    parser.add_argument("-takephoto_topic", type=str, default=TAKEPHOTO_TOPIC,
                        help="Topic name for takephoto subscriber (default: %s)" %TAKEPHOTO_TOPIC)
    parser.add_argument("-savefile", type=str, default=None,
                        help="One shot photo filename (default: None)")
    parser.add_argument('--show', help='show image', action='store_true')


    args = parser.parse_args()
    img_topic = args.image_topic
    img_title = args.savefile
    takephoto_topic = args.takephoto_topic

    # Initialize
    rospy.init_node('takephoto', anonymous=False)
    camera = TakePhoto(img_topic, takephoto_topic)

    # Set output file
    if (img_title is not None):

        print("Taking a photo")

        # Take and save the photo
        camera.take_image(img_title)

        # Sleep to give the last log messages time to be sent
        time.sleep(1)

    elif args.show:

        camera.show_image()

    else:
        print("Set ROS param %s to set image save folder" %PARAM_takephoto_image_folder)
        print("Send String message with data 'get' to topic %s to take a photo" %takephoto_topic)
        print("Send String message with data 'send server port' to topic %s to send image to remote server" %takephoto_topic)
        print("Read param %s for results of server image processing" %PARAM_result)
        print("Running (CTRL-C to quit)")

        rospy.spin()

