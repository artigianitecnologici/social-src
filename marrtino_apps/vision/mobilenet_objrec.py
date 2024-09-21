# Requires Keras and Tensorflow
# python2 -m pip install --user scipy==1.2.1 numpy==1.16.6 tensorflow==1.13.1 keras==2.2.4
# pip install --user opencv-python==3.1.0.5

# For raspberry PI
# swapon
# wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.13.1/tensorflow-1.13.1-cp27-none-linux_armv7l.whl
# sudo -H pip2 install tensorflow-1.13.1-cp27-none-linux_armv7l.whl 


import os, sys, time, socket
import threading

import numpy as np
import json
import argparse
import cv2
import tensorflow as tf
import tensorflow.keras

from tensorflow.keras import utils
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import imagenet_utils, mobilenet

from imageserver import ImageServer

categories = [
    ['banana', 'slug'], ['orange', 'ping-pong_ball'], 
    ['pineapple'], ['cup', 'coffee_mug', 'coffeepot'], ['water_bottle', 'wine_bottle'],
    ['plastic_bag'],
    ['volleyball','tennis_ball','soccer_ball',
     'rugby_ball','basketball','football_helmet'],
    ['teddy', 'toy_poodle'],
    ['computer_keyboard']
 ]


class MNetObjRec:

    def __init__(self):
        print('Loading mobilenet model...')
        self.mnet = mobilenet.MobileNet()   # define the mobilenet model (not thread safe!!!)
        self.flat_categories = [y for x in categories for y in x]
        self.imagenet_idx = {}
        self.getimagenetclasses()
        print('Loading mobilenet model...Done')

    def getimagenetclasses(self):
        print('Get imagenet classes...')
        CLASS_INDEX_PATH = ('https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json')
        
        fpath = utils.get_file(
            'imagenet_class_index.json',
            CLASS_INDEX_PATH,
            cache_subdir='models',
            file_hash='c2c37ea517e94d9795004a39431a14cb')
        with open(fpath) as f:
            CLASS_INDEX = json.load(f)

        #print(CLASS_INDEX)
        
        for k in CLASS_INDEX:
            c = CLASS_INDEX[k][1]
            if c in self.flat_categories:
                self.imagenet_idx[c] = int(k)
                #print('%s: %d' %(c,int(k)))

               
    # process an image to be mobilenet friendly 224x224x3
    def process_image(self,img_path):
      try:
          img = image.load_img(img_path, target_size=(224, 224))
          img_array = image.img_to_array(img)
          img_array = np.expand_dims(img_array, axis=0)
          pImg = mobilenet.preprocess_input(img_array)
          return pImg
      except:
          print("Error in opening image file %s" %img_path)
          return None


    def evalCVImage(self, img):
        imfile = '/tmp/lastimage.png'
        cv2.imwrite(imfile, img)
        return self.evalImageFile(imfile)


    def evalImageFile(self, imfile):
        # pre-process the test image
        pImg = self.process_image(imfile)
        return self.evalImage(pImg)


    def evalImage(self, pImg):

        if pImg is None:  # not an image
            return None  

        nImg = pImg / 255.0 # mobilenet
        aImg = np.array([nImg])  # mobilenet

        # make predictions on test image using mobilenet
        prediction = self.mnet.predict(aImg)
        # obtain the top-5 predictions
        results = imagenet_utils.decode_predictions(prediction)

        sr = '=== Image Classification ==='

        sr += '\n  ImageNet labels: '
        for rs in results[0]:
            sr += '%s: %.2f, ' %(rs[1],rs[2]*100)

        sr += '\n  Knonw labels: '
        
        pbest = 0
        for c in categories:
            p = 0
            for k in c:
                i = self.imagenet_idx[k]
                p += prediction[0][i]
            sr += ' %s: %.2f ' %(c[0],p*100)
            if p>pbest:
                pbest = p
                cbest = c[0]
        sr += '\n  >>> %s %.2f <<<\n' %(cbest,pbest*100)
        print(sr)
        return cbest,pbest*100


mnet = None

def mnet_predict(img):
    global mnet
    if mnet is None:
        mnet = MNetObjRec()
    if isinstance(img,str):
        (c,p) = mnet.evalImageFile(img)
    else:
        (c,p) = mnet.evalImage(img)       
    print("Predicted: %s, prob: %.3f" %(c,p))
    res = "%s;%.3f" %(c,p)
    return res



# wait for Keyboard interrupt
def dospin():
    run = True
    while (run):
        try:
            time.sleep(120)
        except KeyboardInterrupt:
            print("Exit")
            run = False




# main function
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='MobileNet-ImageNet')
    parser.add_argument('-image', type=str, default=None, help='image file')
    parser.add_argument('--server', help='start server', action='store_true')
    parser.add_argument('--init', help='init net', action='store_true')

    args = parser.parse_args()

    # mobilenet server port    
    mnetport=9300

    if args.image is not None:
        print('Predict image %s' %args.image)
        mnet = MNetObjRec()
        r = mnet.evalImageFile(args.image)
        print(r)

    if args.server:
        imgserver = ImageServer(mnetport)
        imgserver.set_predict_cb_fn(mnet_predict)
        imgserver.start()
        dospin() 
        imgserver.stop()
    elif args.init:
        # init net
        mnet = MNetObjRec()


    sys.exit(0)

