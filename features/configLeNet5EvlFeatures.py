# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path
from base import (QApplication,QCursor,QObject,QWidget, QFrame, Qt, QTabWidget, QTextEdit,  QLabel, QIcon, QPushButton,  QInputDialog,QHBoxLayout, QVBoxLayout, 
                                     QGridLayout, QTableWidgetItem, PicLabel, ScrollArea, VBoxLayout, HBoxLayout, pyqtSignal)
from leNet5EvlThread import LeNet5EvlThread
#实现功能与界面的连接整合
class ConfigLeNet5Evl(QObject):

    def __init__(self,leNet5EvlContent):
        super(ConfigLeNet5Evl,self).__init__()
        self.evlContent=leNet5EvlContent
        self.bindConnet()
        self.evlThread=LeNet5EvlThread(self.evlContent)
        
    def bindConnet(self):
        self.evlContent.paraWidget.changeButton.clicked.connect(self.changeStatus)
        
    def changeStatus(self):
        
        self.evlContent.paraWidget.isRunningThread=not self.evlContent.paraWidget.isRunningThread
        if not self.evlContent.paraWidget.isRunningThread:
            self.evlContent.paraWidget.changeButton.setText("开始评估")         
            self.evlThread.setEvlStop()
        elif self.evlContent.paraWidget.isRunningThread:
            self.evlContent.matplotWidget.baseMpl.re_figure_accuracy()
            self.evlContent.paraWidget.changeButton.setText("停止评估")
            self.evlThread=LeNet5EvlThread(self.evlContent)
            #必须重新链接信号
            self.evlThread.oneEvlOverSin.connect(self.evlContent.matplotWidget.baseMpl.update_figure_accuracy)
            self.evlThread.oneEvlOverSin.connect(self.evlDetailsShow)
            
            self.evlThread.finishedEvlSin.connect(self.reSetEvlStatus)
            self.evlThread.start()
            
    def reSetEvlStatus(self):
        
        self.evlContent.paraWidget.changeButton.setText("开始评估"
        )
        self.evlContent.paraWidget.isRunningThread=not self.evlContent.paraWidget.isRunningThread
        
    def evlDetailsShow(self,dict):
        self.evlContent.disDetailsText.append(dict['message'])
