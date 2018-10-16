# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'resnetiv2')
] + sys.path
from base import (itv2time ,QObject,QInputDialog, QTimer,QThread)
from resnetIv2TrainThread import ResnetIv2TrainThread

timeCount=1000
reSetDo=100

isTestSelf=True

#Resnet Inception v2训练界面与功能整合连接
class ConfigResnetIv2Train(QObject):

    def __init__(self,resnetIv2TrainContent,parent=None):
        super(ConfigResnetIv2Train,self).__init__()
        self.trainContent=resnetIv2TrainContent
        self.parent=None
        self.numSteps=2
        self.bindConnet()
        self.runNum=0.0
        self.reSetNum=0
        self.trainTimer=None
        self.trainThread=ResnetIv2TrainThread(self.trainContent)
        self.runThread=None
        
    def bindConnet(self):
        self.trainContent.paraWidget.changeButton.clicked.connect(self.changeStatus)
        self.trainContent.paraWidget.numStepButton.clicked.connect(self.showDialog)
        
    def changeStatus(self):
        #训练时单击则停止
        if self.trainContent.paraWidget.isRunningThread:
            self.trainThread.setTrainStop()
            self.runThread.exit()
            self.runThread.wait()
            self.trainContent.paraWidget.changeButton.setText("开始训练")
            self.trainContent.paraWidget.numStepButton.setEnabled(True)
            self.trainTimer=None
            
        #不在训练时单击则开始训练
        elif not self.trainContent.paraWidget.isRunningThread:
            self.runNum=0.0
            self.trainContent.paraWidget.runTimeLabel.setText(itv2time(self.runNum))
            self.trainContent.disDetailsText.setText("")
            self.trainTimer=QTimer()
            self.trainTimer.start(timeCount)
            self.trainTimer.timeout.connect(self.showTrainRun)
            self.trainContent.matplotWidget.baseMpl.re_figure()
          #  self.trainContent.paraWidget.changeButton.setEnabled(False)
            self.trainContent.paraWidget.changeButton.setText("停止训练")
            self.trainContent.paraWidget.numStepButton.setEnabled(False)
            
            self.trainThread=ResnetIv2TrainThread(self.trainContent)
            self.trainThread.someStepsOverSin.connect(self.trainContent.matplotWidget.baseMpl.update_figure)
            self.trainThread.someStepsOverSin.connect(self.disDetailsShow)
            self.trainThread.finishedTrainSin.connect(self.reSetTrainStatus)
            self.trainThread.runningSin.connect(self.showTrainRun)
            self.trainThread.setNumSteps(self.numSteps)
            self.runThread=QThread()
            self.trainThread.moveToThread(self.runThread)
            self.runThread.started.connect(self.trainThread.run)
            self.runThread.start()

            
        #最后更正状态
        self.trainContent.paraWidget.isRunningThread=not self.trainContent.paraWidget.isRunningThread

    def showDialog(self):
        text, ok = QInputDialog.getInt(self.trainContent.paraWidget, '修改参数', '输入：',min=1)
        if ok:
            self.strNumSteps=str(text)
            self.trainContent.paraWidget.numStepLabel.setText(self.strNumSteps)
            self.numSteps=text
            
    def reSetTrainStatus(self):
        self.trainContent.paraWidget.changeButton.setText("开始训练")
        self.trainContent.paraWidget.numStepButton.setEnabled(True)
        self.runThread.exit()
        self.runThread.wait()
        self.trainContent.paraWidget.runTimeLabel.setText(itv2time(self.runNum))
        

                #最后更正状态
        self.trainContent.paraWidget.isRunningThread=not self.trainContent.paraWidget.isRunningThread
    def disDetailsShow(self,dict):
        if self.reSetNum >=reSetDo:
            self.trainContent.disDetailsText.setText("")
        self.predic_str=str(dict['predictions'])
        self.labels_str=str(dict['labels'])
        self.message="Step %d: loss  %g,prediction:%s,true_labels:%s" % (dict['step'],dict['loss'],self.predic_str,self.labels_str)
        self.trainContent.disDetailsText.append(self.message)
        self.reSetNum=self.reSetNum+1

    def showTrainRun(self):
        
        if self.runThread.isRunning():
            self.runNum=self.runNum+1
            self.trainContent.paraWidget.runTimeLabel.setText(itv2time(self.runNum))
        else:
            self.trainTimer=None

