# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'utils')
] + sys.path
from base import (itv2time ,QObject,QInputDialog, QTimer,QThread,QFileDialog)
from resizeImagesThread import ResizeImagesThread
timeCount=1000
isTestSelf=True
#图片尺寸重置功能与界面整合连接
class ConfigResizeImages(QObject):

    def __init__(self,resizeImgContent,parent=None):
        super(ConfigResizeImages,self).__init__()
        self.resizeImgContent=resizeImgContent
        self.bindConnet()
        self.runNum=0.0
        self.resizeWidth=32
        self.resizeHeight=32
        self.saveDir=None
        self.dataDir=None
        self.resizeImgThread=None
        self.runThread=None
        
    def bindConnet(self):
        self.resizeImgContent.resizeWidthButton.clicked.connect(self.setResizeWidth)
        self.resizeImgContent.resizeHeightButton.clicked.connect(self.setResizeHeight)
        self.resizeImgContent.saveDirButton.clicked.connect(self.setSaveDir)
        self.resizeImgContent.dataDirButton.clicked.connect(self.setDataDir)
        self.resizeImgContent.runTimeButton.clicked.connect(self.setRunTime)

    def setResizeWidth(self):
        text, ok = QInputDialog.getInt(self.resizeImgContent, '修改', '输入：',min=1)
        if ok:
            self.strResizeWidth=str(text)
            self.resizeImgContent.resizeWidthLabel.setText(self.strResizeWidth)
            self.resizeWidth=text

    
    def setResizeHeight(self):
        text, ok = QInputDialog.getInt(self.resizeImgContent, '修改', '输入：',min=1)
        if ok:
            self.strResizeHeight=str(text)
            self.resizeImgContent.resizeHeightLabel.setText(self.strResizeHeight)
            self.resizeHeight=text
        
    def setSaveDir(self):
        self.folder = QFileDialog()
        self.saveDir = self.folder.getExistingDirectory()
        self.saveDir_str=os.path.split(os.path.realpath(self.saveDir))[1]
        if self.saveDir:
            self.resizeImgContent.dataDirButton.setEnabled(True)
            self.resizeImgContent.saveDirLabel.setText(self.saveDir_str)
            

    def setDataDir(self):
        self.folder = QFileDialog()
        self.dataDir = self.folder.getExistingDirectory()
        self.dataDir_str=os.path.split(os.path.realpath(self.dataDir))[1]
        if self.dataDir:
            self.resizeImgContent.runTimeButton.setEnabled(True)
            self.resizeImgContent.dataDirLabel.setText(self.dataDir_str)

            
        
    def setRunTime(self):
        
   
        #如果是在执行，则此时Button Text为停止，更改为开始
        if self.resizeImgContent.isRunningThread:
            self.resizeImgContent.runTimeButton.setText("  开始 " )
            try:
                self.resizeImgThread.exit()
                self.resizeImgThread.wait()
                self.runThread.exit()
                self.runThread.wait()
            except exception as e:
                print(e)
            self.resizeImgContent.isRunningThread=False

        #如果还没开始更改为在停止：
        elif not self.resizeImgContent.isRunningThread:
            self.runNum=0.0
            self.resizeImgContent.runTimeLabel.setText(itv2time(self.runNum))
            self.resizeImgContent.runTimeButton.setText("  生成中  ")
            self.resizeImgContent.runTimeButton.setEnabled(False)#因为多线程停止按钮不好用改为不能停止
            self.resizeImgContent.messageLabel.setText("新文件生成中。。。")
                                                     
            self.resizeImgTimer=QTimer()
            self.resizeImgTimer.start(timeCount)
            self.resizeImgTimer.timeout.connect(self.showTfMakeRun)
            
            self.resizeImgThread=ResizeImagesThread()
            self.resizeImgThread.setResizeWidth(self.resizeWidth)
            self.resizeImgThread.setResizeHeight(self.resizeHeight)
            self.resizeImgThread.setSaveDir(self.saveDir)
            self.resizeImgThread.setDataDir(self.dataDir)
            self.resizeImgThread.runningSin.connect(self.messageShow)
            self.resizeImgThread.finishedSin.connect(self.reSetTfMakeStatus)
            
            self.runThread=QThread()
            self.resizeImgThread.moveToThread(self.runThread)
            self.runThread.started.connect(self.resizeImgThread.run)
            self.runThread.start()
            self.resizeImgContent.isRunningThread=True

        if isTestSelf:
            print("isRuning:",self.resizeImgContent.isRunningThread)
            
    def reSetTfMakeStatus(self,str):
        try:
            self.resizeImgThread.quit()
            self.resizeImgThread.wait()
            self.runThread.exit()
            self.runThread.wait()
            self.resizeImgContent.runTimeButton.setText("  开始  ")
            self.resizeImgContent.runTimeButton.setEnabled(True)
            self.resizeImgContent.messageLabel.setText(str)
            self.resizeImgContent.isRunningThread=not self.resizeImgContent.isRunningThread 
        except exception as e:
            print(e)
              

    def showTfMakeRun(self):
        if self.runThread.isRunning():
            self.runNum=self.runNum+1.0
            self.resizeImgContent.runTimeLabel.setText(itv2time(self.runNum))
        else:
            self.resizeImgTimer=None

    def messageShow(self,str):
        self.resizeImgContent.messageLabel.setText(str)
      
