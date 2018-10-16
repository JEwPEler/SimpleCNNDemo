# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'resnetiv2')
] + sys.path
from base import (itv2time ,QObject,QInputDialog, QTimer,QThread)
from resnetIv2EvlThread import ResnetIv2EvlThread
timeCount=1000
reSetCount=100000.0
#Resnet Inception v2网络功能与界面整合连接
class ConfigResnetIv2Evl(QObject):

    def __init__(self,resnetIv2EvlContent):
        super(ConfigResnetIv2Evl,self).__init__()
        self.evlContent=resnetIv2EvlContent
        self.bindConnet()
        self.runNum=0.0
        self.evlThread=None
        self.runThread=None
        
    def bindConnet(self):
        self.evlContent.paraWidget.changeButton.clicked.connect(self.changeStatus)
        
    def changeStatus(self):
        
        self.evlContent.paraWidget.isRunningThread=not self.evlContent.paraWidget.isRunningThread
        #如果更改后不是在评估
        if not self.evlContent.paraWidget.isRunningThread:
            self.evlContent.paraWidget.changeButton.setText("开始评估")
            try:
                self.evlThread.exit()
                self.evlThread.wait()
                self.runThread.exit()
                self.runThread.wait()
            except exception as e:
                print(e)
        #如果更改为在评估：
        elif self.evlContent.paraWidget.isRunningThread:
            self.runNum=0.0
            self.evlContent.paraWidget.runTimeLabel.setText(itv2time(self.runNum))

            self.evlContent.matplotWidget.baseMpl.re_figure_accuracy()
            self.evlContent.paraWidget.changeButton.setText("停止评估")
            self.evlTimer=QTimer()
            self.evlTimer.start(timeCount)
            #重新连接
            self.evlTimer.timeout.connect(self.showEvlRun)
            self.evlThread=ResnetIv2EvlThread(self.evlContent)
            #必须重新链接信号
            self.evlThread.oneEvlOverSin.connect(self.evlContent.matplotWidget.baseMpl.update_figure_accuracy)
            self.evlThread.oneEvlOverSin.connect(self.evlDetailsShow)
            self.evlThread.runningSin.connect(self.evlInfoShow)
            self.evlThread.finishedEvlSin.connect(self.reSetEvlStatus)
            self.runThread=QThread()
            self.evlThread.moveToThread(self.runThread)
            self.runThread.started.connect(self.evlThread.run)
            self.runThread.start()
            
    def reSetEvlStatus(self):
        try:
            self.evlThread.quit()
            self.evlThread.wait()
            self.runThread.exit()
            self.runThread.wait()
            self.evlContent.paraWidget.changeButton.setText("开始评估")
            self.evlContent.paraWidget.isRunningThread=not self.evlContent.paraWidget.isRunningThread 
        except exception as e:
            print(e)
              

    def evlDetailsShow(self,dict):
        self.evlContent.disDetailsText.append(dict['message'])

    def showEvlRun(self):
        if self.runThread.isRunning():
            self.runNum=self.runNum+1.0
            self.evlContent.paraWidget.runTimeLabel.setText(itv2time(self.runNum))
        else:
            self.evlTimer=None

    def evlInfoShow(self,str):
        self.evlContent.disDetailsText.append(str)
            
