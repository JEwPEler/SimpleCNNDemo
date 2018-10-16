# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'utils')
] + sys.path
from base import (itv2time ,QObject,QInputDialog, QTimer,QThread,QFileDialog)
from tfRecordMakeThread import TFRecordMakeThread
timeCount=1000
#TFRecord制作界面与功能整合连接
class ConfigTFRecordMake(QObject):

    def __init__(self,tfrMakeContent,parent=None):
        super(ConfigTFRecordMake,self).__init__()
        self.tfrMakeContent=tfrMakeContent
        self.bindConnet()
        self.runNum=0.0
        self.numVali=100
        self.numShards=5
        self.saveDir=None
        self.dataDir=None
        self.tfrMakeThread=None
        self.runThread=None
        
    def bindConnet(self):
        self.tfrMakeContent.numValiButton.clicked.connect(self.setNumVali)
        self.tfrMakeContent.numShardsButton.clicked.connect(self.setNumShards)
        self.tfrMakeContent.saveDirButton.clicked.connect(self.setSaveDir)
        self.tfrMakeContent.dataDirButton.clicked.connect(self.setDataDir)
        self.tfrMakeContent.runTimeButton.clicked.connect(self.setRunTime)

    def setNumVali(self):
        text, ok = QInputDialog.getInt(self.tfrMakeContent, '修改验证文件数', '输入：',min=1)
        if ok:
            self.strNumVali=str(text)
            self.tfrMakeContent.numValiLabel.setText(self.strNumVali)
            self.numVali=text

    
    def setNumShards(self):
        text, ok = QInputDialog.getInt(self.tfrMakeContent, '修改验证文件数', '输入：',min=1)
        if ok:
            self.strNumShards=str(text)
            self.tfrMakeContent.numShardsLabel.setText(self.strNumShards)
            self.numShards=text
        
    def setSaveDir(self):
        self.folder = QFileDialog()
        self.saveDir = self.folder.getExistingDirectory()
        self.saveDir_str=os.path.split(os.path.realpath(self.saveDir))[1]
        if self.saveDir:
            self.tfrMakeContent.dataDirButton.setEnabled(True)
            self.tfrMakeContent.saveDirLabel.setText(self.saveDir_str)
            

    def setDataDir(self):
        self.folder = QFileDialog()
        self.dataDir = self.folder.getExistingDirectory()
        self.dataDir_str=os.path.split(os.path.realpath(self.dataDir))[1]
        if self.dataDir:
            self.tfrMakeContent.runTimeButton.setEnabled(True)
            self.tfrMakeContent.dataDirLabel.setText(self.dataDir_str)

            
        
    def setRunTime(self):
        
   
        #如果是在执行，则此时Button Text为停止，更改为开始
        if self.tfrMakeContent.isRunningThread:
            self.tfrMakeContent.runTimeButton.setText("  开始 " )
            try:
                self.tfrMakeThread.exit()
                self.tfrMakeThread.wait()
                self.runThread.exit()
                self.runThread.wait()
            except exception as e:
                print(e)

        #如果还没开始更改为在停止：
        elif not self.tfrMakeContent.isRunningThread:
            self.runNum=0.0
            self.tfrMakeContent.runTimeLabel.setText(itv2time(self.runNum))
            self.tfrMakeContent.runTimeButton.setText("  生成中  ")
            self.tfrMakeContent.messageLabel.setText("TFRecord文件生成中。。。")
            self.tfrMakeContent.runTimeButton.setEnabled(False)#因为多线程停止按钮不好用改为不能停止                                    
            self.tfrMakeTimer=QTimer()
            self.tfrMakeTimer.start(timeCount)
            self.tfrMakeTimer.timeout.connect(self.showTfMakeRun)
            
            self.tfrMakeThread=TFRecordMakeThread()
            self.tfrMakeThread.setNumVali(self.numVali)
            self.tfrMakeThread.setNumShards(self.numShards)
            self.tfrMakeThread.setSaveDir(self.saveDir)
            self.tfrMakeThread.setDataDir(self.dataDir)
            self.tfrMakeThread.runningSin.connect(self.messageShow)
            self.tfrMakeThread.finishedSin.connect(self.reSetTfMakeStatus)
            
            self.runThread=QThread()
            self.tfrMakeThread.moveToThread(self.runThread)
            self.runThread.started.connect(self.tfrMakeThread.run)
            self.runThread.start()

            self.tfrMakeContent.isRunningThread=not self.tfrMakeContent.isRunningThread

    def reSetTfMakeStatus(self,str):
        try:
            self.tfrMakeThread.quit()
            self.tfrMakeThread.wait()
            self.runThread.exit()
            self.runThread.wait()
            self.tfrMakeContent.runTimeButton.setText("  开始  ")
            self.tfrMakeContent.runTimeButton.setEnabled(True)
            self.tfrMakeContent.messageLabel.setText(str)
            self.tfrMakeContent.isRunningThread=not self.tfrMakeContent.isRunningThread 
        except exception as e:
            print(e)
              

    def showTfMakeRun(self):
        if self.runThread.isRunning():
            self.runNum=self.runNum+1.0
            self.tfrMakeContent.runTimeLabel.setText(itv2time(self.runNum))
        else:
            self.tfrMakeTimer=None

    def messageShow(self,str):
        self.tfrMakeContent.messageLabel.setText(str)
      
