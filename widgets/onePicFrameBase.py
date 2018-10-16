# -*- coding: utf-8 -*-

"""基础单图预测界面"""
from base import (QApplication,QCursor,QWidget, QFrame, Qt, QTabWidget, QTextEdit,  QLabel, QIcon, QPushButton, QHBoxLayout, QVBoxLayout, 
                                     QGridLayout, QTableWidgetItem, PicLabel, ScrollArea, VBoxLayout, HBoxLayout, pyqtSignal)
import os 
import sys
import asyncio
from quamash import QEventLoop

myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,"QSS")
] + sys.path

#单图预测基础图
class OnePicFrameBase(ScrollArea):
    def __init__(self, parent=None):
        super(OnePicFrameBase, self).__init__()
        self.parent = parent
        self.setObjectName('onePicFrameBase')
        with open('QSS/trainFrame.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.setLabels()
        self.setButtons()
        self.setLines()
        self.setLayout()

    # 布局。
    def setLabels(self):
        self.titleLabel = QLabel("单图预测:")

        self.showPicLabel=PicLabel(r'resource/one_pic.jpg',300,300)

        self.resultForeLabel = QLabel(" 预测结果")
        self.resultForeLabel.setObjectName("resultForeLabel")
        self.resultForeLabel.setMaximumHeight(27)

        self.resultLabel = QLabel("Now is None")
        self.resultLabel.setObjectName("resultLabel")
        self.resultLabel.setMaximumHeight(27)
        # self.myMusic.setMaximumHeight(54)

    def setLines(self):    
        self.spaceLine = QFrame(self)
        self.spaceLine.setObjectName("spaceLine")
        self.spaceLine.setFrameShape(QFrame.HLine)
        self.spaceLine.setFrameShadow(QFrame.Plain)
        self.spaceLine.setLineWidth(2)

    def setButtons(self):
        self.selectButton = QPushButton("选择图片")
        self.selectButton.setObjectName('selectButton')

        self.startPredicButton=QPushButton("开始测试")
        self.startPredicButton.setObjectName('startPredicButton')
        self.startPredicButton.setEnabled(False)

    def setLayout(self):
        self.mainLayout = VBoxLayout(self)
        
        self.topShowLayout = HBoxLayout()
        self.topShowLayout.addSpacing(20)
        self.topShowLayout.addWidget(self.titleLabel)
        self.topShowLayout.addWidget(self.selectButton)

        self.mainLayout.addLayout(self.topShowLayout)
        
        self.mainLayout.addWidget(self.spaceLine)
        
        self.showPicLayout=HBoxLayout()
        self.showPicLayout.addStretch()
        self.showPicLayout.addWidget(self.showPicLabel)        
        self.showPicLayout.addStretch()

        self.mainLayout.addLayout(self.showPicLayout)
        
        self.resultShowLayout = HBoxLayout()
        self.resultShowLayout.addStretch()
        self.resultShowLayout.addWidget(self.resultForeLabel)        
        self.resultShowLayout.addWidget(self.resultLabel)
        self.resultShowLayout.addStretch()

        
        self.mainLayout.addLayout(self.resultShowLayout)

        self.startPredicLayout=HBoxLayout()
        self.startPredicLayout.addStretch()
        self.startPredicLayout.addWidget(self.startPredicButton)        
        self.startPredicLayout.addStretch()
        self.mainLayout.addLayout(self.startPredicLayout)
        self.mainLayout.addStretch(1)

        
if __name__ == '__main__':
    os.chdir("..")
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=OnePicFrameBase()
#    main.config=ConfigOnePic(main)
    main.titleLabel.setText("LeNet5单图预测")
   
    main.show()
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)

 
