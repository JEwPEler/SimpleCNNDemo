# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'resnetiv2')
] + sys.path
from resnetIv2TrainThread import image_size
thisFolder = os.path.split(os.path.realpath(__file__))[0]
label_lookup_path  =os.path.join(thisFolder, "/log/graph.pbtxt")
uid_lookup_path =os.path.join(thisFolder, "./dataset/labels.txt")
default_test_src='./dataset/traffic_sign_photos/0008_注意合流右/00018.jpg'
checkpoint_dir=os.path.join(thisFolder,"log")
default_test_path=os.path.join(thisFolder,"dataset/traffic_sign_photos/0000_﻿十字交叉路口1/00012.jpg")

labels_file = os.path.join(thisFolder, 'dataset/labels.txt')
labels = open(labels_file, 'r',encoding='UTF-8')
#Create a dictionary to refer each label to their string name
labels_to_name = {}

for line in labels:
    label, string_name = line.split(':')
    string_name = string_name[:-1] #Remove newline
    labels_to_name[int(label)] = string_name


NUM_CHANNELS = 3

isTestSelf=True

#import json
#import math
import time
import numpy as np
import tensorflow as tf
from nets import nets_factory
from preprocessing import preprocessing_factory
from base import ( QThread,pyqtSignal, QApplication,QWidget)

slim = tf.contrib.slim

tf.app.flags.DEFINE_string(
    'master', '', 'The address of the TensorFlow master to use.')
tf.app.flags.DEFINE_string(
    'checkpoint_path', checkpoint_dir,
    'The directory where the model was written to or an absolute path to a '
    'checkpoint file.')

#tf.app.flags.DEFINE_integer(
 #   'batch_size', 16, 'Batch size.')
tf.app.flags.DEFINE_integer(
    'num_classes', 8, 'Number of classes.')
tf.app.flags.DEFINE_integer(
    'labels_offset', 0,
    'An offset for the labels in the dataset. This flag is primarily used to '
    'evaluate the VGG and ResNet architectures which do not use a background '
    'class for the ImageNet dataset.')
tf.app.flags.DEFINE_string(
    'model_name', 'inception_resnet_v2', 'The name of the architecture to evaluate.')
tf.app.flags.DEFINE_string(
    'preprocessing_name', None, 'The name of the preprocessing to use. If left '
    'as `None`, then the model_name flag is used.')
tf.app.flags.DEFINE_integer(
    'test_image_size', image_size, 'Eval image size')

FLAGS = tf.app.flags.FLAGS

class ResnetIv2OnePicThread(QThread):

    resultSin=pyqtSignal(str)
    runningSin=pyqtSignal(str)

    def __init__(self,parent=None):
        super(ResnetIv2OnePicThread,self).__init__()
        self.parent=parent
        self.test_path = default_test_path

    def setSrc(self,test_path):
        
        self.test_path=test_path

    def run(self):
        tf.logging.set_verbosity(tf.logging.INFO)
        with tf.Graph().as_default():
            tf_global_step = slim.get_or_create_global_step()
            network_fn = nets_factory.get_network_fn(
                FLAGS.model_name,
                num_classes=FLAGS.num_classes,
                is_training=False)
            preprocessing_name = FLAGS.preprocessing_name or FLAGS.model_name
            image_preprocessing_fn = preprocessing_factory.get_preprocessing(
                preprocessing_name,
                is_training=False)
            test_image_size = FLAGS.test_image_size or network_fn.default_image_size
            if tf.gfile.IsDirectory(FLAGS.checkpoint_path):
                checkpoint_path = tf.train.latest_checkpoint(FLAGS.checkpoint_path)
            else:
                checkpoint_path = FLAGS.checkpoint_path
            tensor_input = tf.placeholder(tf.float32, [1, test_image_size, test_image_size, 3])
            logits, _ = network_fn(tensor_input)
            prediction_label = tf.argmax(logits, 1)
            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                saver = tf.train.Saver()
                saver.restore(sess, checkpoint_path)
                time_start = time.time()
                images=list()
               
                image = open(self.test_path, 'rb').read()
                if isTestSelf:
                    print(self.test_path)
                image = tf.image.decode_jpeg(image, channels=3)
                processed_image = image_preprocessing_fn(image, test_image_size, test_image_size)
                processed_image = sess.run(processed_image)
                images.append(processed_image)
                images = np.array(images)
                predictions = sess.run(prediction_label, feed_dict = {tensor_input : images})
                self.resultSin.emit(labels_to_name[predictions[0]])
                if isTestSelf:
                    print(predictions)
                    print(labels_to_name[predictions[0]])
                    time_total = time.time() - time_start
                    print('total time: {}'.format(  time_total))


                    

class Main(QWidget):  
    def __init__(self, parent = None):  
        super(Main,self).__init__(parent)  
  
        ##创建一个线程实例并设置名称、变量、信号槽  
        self.thread = ResnetIv2OnePicThread(self)
        #self.thread.setSrc(default_test_src)
        self.one_test_path="F:\\pelfiles\\workstation\\python\pycode\\gradu\\self\\try_cod\\try_7_test_multi_threath\\TrafficSignsClassicy\\resource\\evling.jpg"
        self.thread.setSrc(self.one_test_path)
        self.thread.start()
        print("this is a return")
        if isTestSelf:
            print(sys.path)


        
if __name__ == "__main__":
    app = QApplication([])  
  
    main = Main()  
    main.show()  
  
    app.exec_()  
    print('main start!please wait')
    self_start_time = time.time()
    self_end_time=time.time()
    print("total use:",self_end_time-self_start_time)
