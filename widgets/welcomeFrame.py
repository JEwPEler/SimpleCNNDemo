# -*- coding: utf-8 -*-
from base import (QApplication,QCursor,QWidget, QFrame, Qt, QTabWidget, QTextEdit,  QLabel, QIcon, QPushButton, QHBoxLayout, QVBoxLayout, 
                                     QGridLayout, QTableWidgetItem, PicLabel, ScrollArea, VBoxLayout, HBoxLayout, pyqtSignal)
import os 
import sys
import asyncio
from quamash import QEventLoop

from matplotForPyqt5 import NavToolbar,PyqtMplCanvas

# 最初的界面，方便构建。
class WelcomeFrame(ScrollArea):
  
    def __init__(self, parent=None):
        """
        主内容区，显示初始界面
        目前只显示一个label
        """
        super(WelcomeFrame, self).__init__()
        self.parent = parent
        self.setObjectName("WelcomeFrame")

        # 连接导航栏的按钮。
        # self.parent.navigation.naviLeNet5ListFunction = self.naviLeNet5ListYFunction
        with open("QSS/mainContent.qss", 'r', encoding='utf-8') as f:
            self.style = f.read()
            self.setStyleSheet(self.style)
        # 加载按钮设置。
        self.setButtons()
        # 加载标签设置。
        self.setLabels()
        # 加载布局设置。
        self.setLayouts()

    # 布局。
    def setButtons(self):
        """创建所有的按钮。"""
        pass


    def setLabels(self):
        """创建所需的所有标签。"""

        self.welcomeLabel = QLabel(self)
        self.welcomeLabel.setText("<b>主界面</b>")
        self.welcomeLabel.setMaximumWidth(1000)
        self.welcomeLabel.setMaximumHeight(500)
        self.welcomeLabel.setMinimumHeight(100)
        

    def setLayouts(self):
        """设置布局。"""
        self.mainLayout = VBoxLayout()

        self.contentLayout = HBoxLayout()
        self.contentLayout.addStretch(100)
        self.contentLayout.addWidget(self.welcomeLabel)
        self.contentLayout.addStretch(100)
        self.contentLayout.setStretch(0,1)
        self.contentLayout.setStretch(1,1)
        self.contentLayout.setStretch(2,1)

        self.mainLayout.addLayout(self.contentLayout)

        self.frame.setLayout(self.mainLayout)
    
        
if __name__ == '__main__':
    os.chdir("..")
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=WelcomeFrame()
    main.welcomeLabel.setText("welcome")
   
    main.show()
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)

