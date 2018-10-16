# -*- coding: utf-8 -*-

import time
import tensorflow as tf
import leNet5ImgProcess
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

LEARNING_RATE_BASE = 0.01
LEARNING_RATE_DECAY = 0.99
DECAY_STEP = 500

REGULARAZTION_RATE = 0.0001

MOVING_AVERAGE_DECAY = 0.999

thisFolder = os.path.split(os.path.realpath(__file__))[0]

MODEL_SAVE_PATH =os.path.join(thisFolder,  "model")
MODEL_NAME =  "model.ckpt"
SAVE_MODEL=os.path.join(MODEL_SAVE_PATH,MODEL_NAME)

SUMMARY_DIR = os.path.join(thisFolder, "log")

BATCH = 20
STEPS = 50

isTestSelf=False

class LeNet5TrainThread(QThread):
            
    someStepsOverSin = pyqtSignal(dict)
    finishedTrainSin = pyqtSignal()     

    def __init__(self,parent=None):
        super(LeNet5TrainThread,self).__init__()
        self.parent=parent
        self.STEPS=STEPS
        self.isTraining=True

        if isTestSelf:
            self.someStepsOverSin.connect(self.printSin)
        self.isTrained=False

    def printSin(self,val):
        dic=val
        print(dic["step"]*3)
    def setNumSteps(self,numSteps):
        self.steps=numSteps
        print(self.steps)
        
    def setTrainStop(self):
        self.isTraining=False
        return
        
    def run(self):
 
    #输入输出placeholder
        x_input_holder = tf.placeholder(
            tf.float32,
            [None, leNet5Inference.IMAGE_SIZE,
             leNet5Inference.IMAGE_SIZE, leNet5Inference.NUM_CHANNELS],
            name="InputPlaceholder"
        )
        y_input_holder = tf.placeholder(
            tf.float32,
            [None, leNet5Inference.OUTPUT_NODE],
            name="OutputPlaceholder"
        )
        #指数衰退学习率
        global_step = tf.Variable(0, trainable=False)
        learning_rate = tf.train.exponential_decay(
            LEARNING_RATE_BASE,
            global_step,
            DECAY_STEP,
            LEARNING_RATE_DECAY
        )
        #l2正则化
        regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)
        
        #损失函数为交叉熵
        prediction = leNet5Inference.inference_cnn(x_input_holder, regularizer, 0.5)
        prediction = tf.clip_by_value(prediction, 1e-10, 1e100)
        cross_entropy = tf.reduce_mean(
            -tf.reduce_sum(y_input_holder * tf.log(prediction), reduction_indices=[1])
        )
        loss = cross_entropy + tf.add_n(tf.get_collection("losses"))

        #滑动平均
        variable_averages = tf.train.ExponentialMovingAverage(
            MOVING_AVERAGE_DECAY,
            global_step
        )
        variable_averages_op = variable_averages.apply(tf.trainable_variables())
        if isTestSelf:
            print(MODEL_SAVE_PATH)
            print(SAVE_MODEL)
        

        #梯度下降及反向传播
        train_step = tf.train.GradientDescentOptimizer(learning_rate) \
                             .minimize(loss, global_step=global_step)
        with tf.control_dependencies([train_step, variable_averages_op]):
            train_op = tf.no_op(name="train")

        saver = tf.train.Saver()
        with tf.Session() as sess:
            tf.global_variables_initializer().run()
            #循环self.steps次
            try:
                ckpt=tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
            except:
                pass
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            for i in range(1,self.steps+1):
                if not self.isTraining:
                    return
                if self.isTraining:
                    x_input, y_input = leNet5ImgProcess.get_train_batch(BATCH)
                    _, loss_value = sess.run(
                        [train_op, loss],
                        feed_dict={
                            x_input_holder: x_input,
                            y_input_holder: y_input
                        }
                    )
                    
                    self.isTrained=True
                    if i % 10 == 0 or i  == self.steps:
                        print(
                            "Step %d: loss on training batch is %g."
                            % (i, loss_value)
                        )
                        out_message="Step %d: loss on training batch is %g." % (i, loss_value)
                        self.someStepsOverSin.emit({"step":i,"loss":loss_value, "message":out_message})
                    if i % 5000 == 0 or i  == self.steps :   
                        saver.save(
                            sess,
                            SAVE_MODEL,
                            global_step=global_step
                    )
                elif (not self.isTraining) and (self.isTrained):
                    saver.save(
                            sess,
                            SAVE_MODEL,
                            global_step=global_step
                        )
                elif not self.isTraining:
                    return
            self.finishedTrainSin.emit()

                


class Main(QWidget):  
    def __init__(self, parent = None):  
        super(Main,self).__init__(parent)  
  
        ##创建一个线程实例并设置名称、变量、信号槽  
        self.thread = LeNet5TrainThread(self)
        print(self.thread.isTraining)
        self.thread.setNumSteps(200)
        self.thread.start()
        print("this is a return")
        if isTestSelf:
            print(sys.path)


        
if __name__ == "__main__":
    app = QApplication([])  
  
    main = Main()  
    main.show()  
  
    app.exec_()  
   
