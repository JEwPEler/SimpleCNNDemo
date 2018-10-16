# -*- coding: utf-8 -*-

"""TFRecord制作界面"""
# -*- coding: utf-8 -*-

import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features')
] + sys.path

from base import (QApplication,QWidget,QLabel,ScrollArea,
                  VBoxLayout, HBoxLayout,QPushButton)


from configTFRecordMakeFeatures import ConfigTFRecordMake

import asyncio
from quamash import QEventLoop

isTestingPrint=True

# TFRecord制作界面
class TFRecordMakeFrame(ScrollArea):

    def __init__(self, parent=None):
        super(TFRecordMakeFrame, self).__init__()

        # self.hide()
        self.parent = parent
        self.setObjectName('TFRecordMakeFrame')
        with open('QSS/selfBaseFrame.qss', 'r', encoding='utf-8') as f:
            self.style=f.read()
            self.setStyleSheet(self.style)
        self.isRunningThread=False
        
        self.setLayouts()    
        
    def setNumValiLayout(self):
        """验证集数目设置。"""
        
        self.numValiForeLabel = QLabel('验证集数目:')
        self.numValiForeLabel.setObjectName("numValiForeLabel")
        self.numValiForeLabel.setMaximumWidth(170)
        self.numValiForeLabel.setMinimumWidth(30)
        self.numValiForeLabel.setMaximumHeight(37)

        self.numValiLabel = QLabel('100')
        self.numValiLabel.setObjectName("numValiLabel")
        self.numValiLabel.setMaximumWidth(170)
        self.numValiLabel.setMinimumWidth(30)
        self.numValiLabel.setMaximumHeight(37)
 
        self.numValiButton = QPushButton("  修改  ")
        self.numValiButton.setObjectName('numValiButton')
        self.numValiButton.setMaximumSize(90, 35)

        self.numValiLayout=HBoxLayout()
        self.numValiLayout.addWidget(self.numValiForeLabel)
        self.numValiLayout.addWidget(self.numValiLabel)
        self.numValiLayout.addWidget(self.numValiButton)
        self.numValiLayout.addSpacing(3)

    def setNumShardsLayout(self):
        """生成文件分割数设置。"""
        
        self.numShardsForeLabel = QLabel('文件分割数')
        self.numShardsForeLabel.setObjectName("numShardsForeLabel")
        self.numShardsForeLabel.setMaximumWidth(170)
        self.numShardsForeLabel.setMinimumWidth(30)
        self.numShardsForeLabel.setMaximumHeight(37)

        self.numShardsLabel = QLabel('5')
        self.numShardsLabel.setObjectName("numShardsLabel")
        self.numShardsLabel.setMaximumWidth(170)
        self.numShardsLabel.setMinimumWidth(30)
        self.numShardsLabel.setMaximumHeight(37)

        self.numShardsButton = QPushButton("  修改  ")
        self.numShardsButton.setObjectName('numShardsButton')
        self.numShardsButton.setMaximumSize(90, 35)

        self.numShardsLayout=HBoxLayout()
        self.numShardsLayout.addWidget(self.numShardsForeLabel)
        self.numShardsLayout.addWidget(self.numShardsLabel)
        self.numShardsLayout.addWidget(self.numShardsButton)
        self.numShardsLayout.addSpacing(3)

    def setSaveDirLayout(self):
        """生成文件保存目录"""
        
        self.saveDirForeLabel = QLabel('主目录保存:')
        self.saveDirForeLabel.setObjectName("SaveDirForeLabel")
        self.saveDirForeLabel.setMaximumWidth(170)
        self.saveDirForeLabel.setMinimumWidth(30)
        self.saveDirForeLabel.setMaximumHeight(37)

        self.saveDirLabel = QLabel('TFRecord文件')
        self.saveDirLabel.setObjectName("SaveDirLabel")
        self.saveDirLabel.setMaximumWidth(170)
        self.saveDirLabel.setMinimumWidth(30)
        self.saveDirLabel.setMaximumHeight(37)

        self.saveDirButton = QPushButton("打开目录")
        self.saveDirButton.setObjectName('SaveDirButton')
        self.saveDirButton.setMaximumSize(90, 35)

        self.saveDirLayout=HBoxLayout()
        self.saveDirLayout.addWidget(self.saveDirForeLabel)
        self.saveDirLayout.addWidget(self.saveDirLabel)
        self.saveDirLayout.addWidget(self.saveDirButton)
        self.saveDirLayout.addSpacing(3)

    def setDataDirLayout(self):
        """验证集数目设置。"""
        
        self.dataDirForeLabel = QLabel('次目录提供:')
        self.dataDirForeLabel.setObjectName("dataDirForeLabel")
        self.dataDirForeLabel.setMaximumWidth(170)
        self.dataDirForeLabel.setMinimumWidth(30)
        self.dataDirForeLabel.setMaximumHeight(37)

        self.dataDirLabel = QLabel('分类图像文件')
        self.dataDirLabel.setObjectName("dataDirLabel")
        self.dataDirLabel.setMaximumWidth(170)
        self.dataDirLabel.setMinimumWidth(30)
        self.dataDirLabel.setMaximumHeight(37)

        self.dataDirButton = QPushButton("打开目录")
        self.dataDirButton.setObjectName('dataDirButton')
        self.dataDirButton.setEnabled(False)
        self.dataDirButton.setMaximumSize(90, 35)

        self.dataDirLayout=HBoxLayout()
        self.dataDirLayout.addWidget(self.dataDirForeLabel)
        self.dataDirLayout.addWidget(self.dataDirLabel)
        self.dataDirLayout.addWidget(self.dataDirButton)
        self.dataDirLayout.addSpacing(3)

    def setRunTimeLayout(self):
        
        self.runTimeForeLabel = QLabel('执行时间:')
        self.runTimeForeLabel.setObjectName("runTimeForeLabel")
        self.runTimeForeLabel.setMaximumWidth(170)
        self.runTimeForeLabel.setMinimumWidth(30)
        self.runTimeForeLabel.setMaximumHeight(37)
        
        self.runTimeLabel = QLabel('00:00')
        self.runTimeLabel.setObjectName("runTimeLabel")
        self.runTimeLabel.setMaximumWidth(170)
        self.runTimeLabel.setMinimumWidth(30)
        self.runTimeLabel.setMaximumHeight(37)


        self.runTimeButton = QPushButton(self)
        self.runTimeButton.setObjectName('runTimeButton')
        if not self.isRunningThread:
            self.runTimeButton.setText("开始")
            self.runTimeButton.setEnabled(False)
        elif self.isRunningThread:
            self.runTimeButton.setText("停止")
        self.runTimeButton.setMaximumSize(90,30)

        self.runTimeLayout=HBoxLayout()
        self.runTimeLayout.addWidget(self.runTimeForeLabel)
        self.runTimeLayout.addWidget(self.runTimeLabel)
        self.runTimeLayout.addWidget(self.runTimeButton)
        self.runTimeLayout.addSpacing(3)



    def setLabels(self):
        """创建所需的所有标签。"""

        self.titleLabel =QLabel('tfRecord制作')
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setMaximumWidth(500)
        self.titleLabel.setMinimumWidth(30)
        self.titleLabel.setMaximumHeight(37)
        self.titleLabel.setObjectName('titleLabel')
        
        self.messageLabel =QLabel('不考虑程序错误情况')
        self.messageLabel.setObjectName("messageLabel")
        self.messageLabel.setMaximumWidth(1000)
        self.messageLabel.setMinimumWidth(300)
        self.messageLabel.setMaximumHeight(37)
        self.messageLabel.setObjectName('messageLabel')
        
    def setLayouts(self):
        self.setLabels()
        self.mainLayout = VBoxLayout()
        #训练页标题

        self.mainLayout.addWidget(self.titleLabel)

        self.setNumValiLayout()
        self.setNumShardsLayout()
        self.setSaveDirLayout()
        self.setDataDirLayout()
        self.setRunTimeLayout()
        
        
        self.contentLayout=VBoxLayout()
        self.contentLayout.addLayout(self.numValiLayout)
        self.contentLayout.addLayout(self.numShardsLayout)
        self.contentLayout.addLayout(self.saveDirLayout)
        self.contentLayout.addLayout(self.dataDirLayout)
        self.contentLayout.addLayout(self.runTimeLayout)
        
        self.contentLayout.addStretch(0)
        
        self.mainLayout.addLayout(self.contentLayout)
        
        self.messageLayout=HBoxLayout()
        self.messageLayout.addStretch()
        self.messageLayout.addWidget(self.messageLabel)
        self.messageLayout.addStretch()
        self.messageLayout.setStretch(0, 135)
        self.messageLayout.setStretch(1, 100)
        self.messageLayout.setStretch(2, 100)
        
        self.mainLayout.addLayout(self.messageLayout)
        self.mainLayout.addStretch(1000)
        self.frame.setLayout(self.mainLayout)

        if isTestingPrint:
            print("setLayout is over!")

        
        
if __name__ == '__main__':
    os.chdir("..")
    
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=TFRecordMakeFrame()
    #  main.show()
    main.config=ConfigTFRecordMake(main)

    main.show()
    
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)
