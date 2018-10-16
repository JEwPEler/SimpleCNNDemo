# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path
from base import (QApplication,QCursor,QObject,QWidget, QFrame, Qt, QTabWidget, QTextEdit,  QLabel, QIcon, QPushButton,  QInputDialog,QHBoxLayout, QVBoxLayout, 
                                     QFileDialog, pyqtSignal)
from leNet5OnePicThread import LeNet5OnePicThread

isTestSelf=True
#实现LeNet5单图预测与界面的整合
class ConfigLeNet5OnePic(QObject):

    def __init__(self,leNet5OnePicContent):
        super(ConfigLeNet5OnePic,self).__init__()
        self.onePicContent=leNet5OnePicContent
        
        self.bindConnet()
        self.src=None

    def bindConnet(self):
        self.onePicContent.selectButton.clicked.connect(self.selectPic)
        self.onePicContent.startPredicButton.clicked.connect(self.startPredict)

    def selectPic(self):
        self.onePicContent.startPredicButton.setEnabled(True)
        try:
            self.src=QFileDialog.getOpenFileName(self.onePicContent,'Open file')
            if isTestSelf:
                print (self.src)
            self.onePicContent.showPicLabel.setSrc(self.src[0])
            self.onePicContent.resultLabel.setText("Now is None")
            
        except:
            pass
        
    def showResult(self,str):
        if isTestSelf:
            print ("show ",str)
        self.onePicContent.startPredicButton.setText("开始预测")
        self.onePicContent.startPredicButton.setEnabled(True)
        self.onePicContent.selectButton.setEnabled(True)
        self.onePicContent.resultLabel.setText(str)
            
    def startPredict(self):

        if isTestSelf:
            print ("start ",self.src)
        self.onePicContent.resultLabel.setText("预测中。。。")
        self.onePicContent.startPredicButton.setText("预测中不可用")
        self.onePicContent.startPredicButton.setEnabled(False)
        self.onePicContent.selectButton.setEnabled(False)
        self.onePicThread=LeNet5OnePicThread()
        self.onePicThread.setSrc(self.src[0])
        self.onePicThread.resultSin.connect(self.showResult)
        self.onePicThread.start()
        
