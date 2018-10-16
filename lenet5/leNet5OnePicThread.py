# -*- coding: utf-8 -*-

import tensorflow as tf
import leNet5ImgProcess
import leNet5Inference
import leNet5TrainThread
from PIL import Image
import os
import sys
import asyncio
from quamash import QEventLoop
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')] + sys.path
from base import (QApplication,QWidget,  QThread, pyqtSignal)

thisFolder = os.path.split(os.path.realpath(__file__))[0]
labels_file = os.path.join(thisFolder, 'data32/labels.txt')
labels = open(labels_file, 'r',encoding='UTF-8')
#Create a dictionary to refer each label to their string name
labels_to_name = {}
for line in labels:
    label, string_name = line.split(':')
    string_name = string_name[:-1] #Remove newline
    labels_to_name[int(label)] = string_name


isTestSelf=True

class LeNet5OnePicThread(QThread):

    resultSin=pyqtSignal(str)
    
    def __init__(self,parent=None):
        super(LeNet5OnePicThread,self).__init__()
        self.parent=parent
        default_src='./data32/Testing/00002/00108.jpg'
        self.src=default_src

        if isTestSelf:
            self.resultSin.connect(self.printResult)

    def setSrc(self,src):
        self.src=src

    def printResult(self,int):

        print("result is ",str(int))
        
    def run(self):
        x = tf.placeholder(
            tf.float32,
            [1, leNet5Inference.IMAGE_SIZE,
             leNet5Inference.IMAGE_SIZE, leNet5Inference.NUM_CHANNELS],
            name="x-input"
        )
        y = leNet5Inference.inference_cnn(x)
        prediction_label = tf.argmax(y, 1)
        
        variable_averages = tf.train.ExponentialMovingAverage(
            leNet5TrainThread.MOVING_AVERAGE_DECAY
        )
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)
                        
        with tf.Session() as sess:
            try:
                ckpt=tf.train.get_checkpoint_state(leNet5TrainThread.MODEL_SAVE_PATH)
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    if isTestSelf:
                        print(ckpt)
                        print(ckpt.ckpt.model_checkpoint_path)
                
            except:
                pass
            
            try:
                image = leNet5ImgProcess.read_image_resize(self.src)
                label = sess.run(
                    prediction_label,
                    feed_dict={x: [image]}
                )
                self.resultSin.emit(labels_to_name[label[0]])
                if isTestSelf:
                    print( labels_to_name[label[0]])
            except Exception as e:
                print(e)

class Main(QWidget):  
    def __init__(self, parent = None):  
        super(Main,self).__init__(parent)  

        self.src='./data32/Testing/00003/00429.jpg'
        ##创建一个线程实例并设置名称、变量、信号槽  
        self.thread = LeNet5OnePicThread(self)

        self.thread.setSrc(self.src)

        self.thread.start()


        
if __name__ == "__main__":
    app = QApplication([])  
  
    main = Main()  
    main.show()  
  
    app.exec_()  
   
