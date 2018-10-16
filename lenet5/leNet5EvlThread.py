# -*- coding: utf-8 -*-
'''
神经网络模型评估
'''
import tensorflow as tf
import leNet5ImgProcess
import leNet5TrainThread
import leNet5Inference

import os
import sys
import asyncio
from quamash import QEventLoop
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path
from base import (QApplication,QCursor,QWidget, QFrame, QThread,Qt, QTabWidget, QTextEdit,  QLabel, QIcon, QPushButton,  QInputDialog,QHBoxLayout, QVBoxLayout, 
                                     QGridLayout, QTableWidgetItem, PicLabel, ScrollArea, VBoxLayout, HBoxLayout, pyqtSignal)

isTestSelf=True

CHECKPOINT_PATH=leNet5TrainThread.MODEL_SAVE_PATH


class LeNet5EvlThread(QThread):

    oneEvlOverSin=pyqtSignal(dict)
    finishedEvlSin=pyqtSignal()

    def __init__(self,parent=None):
        super(LeNet5EvlThread,self).__init__()
        self.parent=parent
        self.isEvling=True

        if isTestSelf:
            self.oneEvlOverSin.connect(self.printOneSin)
            self.finishedEvlSin.connect(self.printFinishedSin)
            
        self.isEvled=False

    def setEvlStop(self):
        self.isEvling=False
        
    def printOneSin(self,dict):
        print(dict)

    def printFinishedSin(self):
        print("finished!")
    def run(self):
        x = tf.placeholder(
            tf.float32,
            [None, leNet5Inference.IMAGE_SIZE,
             leNet5Inference.IMAGE_SIZE, leNet5Inference.NUM_CHANNELS],
            name="x-input"
        )
        y_ = tf.placeholder(
            tf.float32,
            [None, leNet5Inference.OUTPUT_NODE],
            name="y-input"
        )
        y = leNet5Inference.inference_cnn(x)
        correct_prediction = tf.equal(
            tf.argmax(y, 1),
            tf.argmax(y_, 1)
        )
        accuracy = tf.reduce_mean(
            tf.cast(correct_prediction, tf.float32)
        )
        variable_averages = tf.train.ExponentialMovingAverage(
            leNet5TrainThread.MOVING_AVERAGE_DECAY
        )
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)

        with tf.Session() as sess:
            if self.isEvling:
                if isTestSelf:
                    print("retore start")
                ckpt=tf.train.get_checkpoint_state(CHECKPOINT_PATH)
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    if isTestSelf:
                        print("retore over")
                        print(ckpt.model_checkpoint_path)
                    for i in range(5):
                        x_test, y_test = leNet5ImgProcess.get_test_set(50)
                        accuracy_score = sess.run(
                            accuracy,
                            feed_dict={
                                x: x_test[:300],
                                y_: y_test[:300]
                            }
                        )
                        out_message="第"+str(i+1)+"次评估模型正解率为:"+str(accuracy_score*100)+"%"
                        self.oneEvlOverSin.emit({'step':i+1,'accuracy_score':accuracy_score,"message":out_message})
                        if isTestSelf:
                            print("%.2f%%" % (accuracy_score * 100))
                elif not self.isEvling:
                    return
        self.finishedEvlSin.emit()
        return


class Main(QWidget):  
    def __init__(self, parent = None):  
        super(Main,self).__init__(parent)  
  
        ##创建一个线程实例并设置名称、变量、信号槽  
        self.thread = LeNet5EvlThread(self)
        print(self.thread.isEvling)
        self.thread.start()


        
if __name__ == "__main__":
    app = QApplication([])  
  
    main = Main()  
    main.show()  
  
    app.exec_()  
   
