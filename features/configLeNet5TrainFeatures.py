# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path
from base import (itv2time ,QObject,QInputDialog, QTimer,QThread)
from leNet5TrainThread import LeNet5TrainThread

timeCount=1000
reSetCount=100000.0
#LeNet5网络训练界面与功能的整合
class ConfigLeNet5Train(QObject):

    def __init__(self,leNet5TrainContent,parent=None,):
        super(ConfigLeNet5Train,self).__init__()
        self.trainContent=leNet5TrainContent
        self.numSteps=50
        self.bindConnet()
        self.parent=None
        self.runNum=0.0
        self.trainTimer=None
        self.trainThread=LeNet5TrainThread()
        self.runThread=None
        
    def bindConnet(self):
        self.trainContent.paraWidget.changeButton.clicked.connect(self.changeTrainStatus)
        self.trainContent.paraWidget.numStepButton.clicked.connect(self.showDialog)
        
    def changeTrainStatus(self):
        #训练时单击则停止
        if self.trainContent.paraWidget.isRunningThread:
            self.trainThread.setTrainStop()
            self.trainContent.paraWidget.changeButton.setText("开始训练")
            self.trainContent.paraWidget.numStepButton.setEnabled(True)
            self.trainThread.quit()
            self.trainThread.wait()
            self.runThread.exit()
            self.runThread.wait()

        #不在训练时单击则开始训练
        elif not self.trainContent.paraWidget.isRunningThread:
            self.runNum=0.0
            self.trainContent.paraWidget.runTimeLabel.setText(itv2time(self.runNum))

            self.trainTimer=QTimer()
            self.trainTimer.start(timeCount)
            #重新连接
            self.trainTimer.timeout.connect(self.showTrainRun)
            self.trainContent.matplotWidget.baseMpl.re_figure()
            self.trainContent.paraWidget.changeButton.setText("停止训练")
            self.trainContent.paraWidget.numStepButton.setEnabled(False)
            self.trainContent.disDetailsText.setText("")
            self.trainThread=LeNet5TrainThread()

            self.trainThread.someStepsOverSin.connect(self.trainContent.matplotWidget.baseMpl.update_figure)
            self.trainThread.someStepsOverSin.connect(self.disDetailsShow)
            self.trainThread.finishedTrainSin.connect(self.reSetTrainStatus)
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
        try:
            self.trainThread.quit()
            self.trainThread.wait()
            self.runThread.exit()
            self.runThread.wait()
            self.trainContent.paraWidget.changeButton.setText("开始训练")
        except exception as e:
            print(e)

        self.trainContent.paraWidget.numStepButton.setEnabled(True)
                #最后更正状态
        self.trainContent.paraWidget.isRunningThread=not self.trainContent.paraWidget.isRunningThread
        self.runThread.exit()
        self.runThread.wait()
    def disDetailsShow(self,dict):
        if self.runNum>=reSetCount:
            self.trainContent.disDetailsText.setText("")
            self.trainContent.matplotWidget.baseMpl.re_figure()
        self.trainContent.disDetailsText.append(dict['message'])

    def showTrainRun(self):
        if self.runThread.isRunning():
            self.runNum=self.runNum+1.0
            self.trainContent.paraWidget.runTimeLabel.setText(itv2time(self.runNum))
        else:
            self.trainTimer=None
