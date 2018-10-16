# -*- coding: utf-8 -*-

"""
主界面设计，多线程注意
# 
"""

import os
import sys
import os.path

myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
            os.path.join(myFolder, 'features'),
            os.path.join(myFolder, 'logger'),
            os.path.join(myFolder,'lenet5'),
            os.path.join(myFolder,'resnetiv2'),
            os.path.join(myFolder,'utils'),
            os.path.join(myFolder,'resources'),
            os.path.join(myFolder,'QSS'),
] + sys.path

os.chdir(myFolder)

import asyncio
import logging

# event loop
# https://github.com/harvimt/quamash
# an asyncio eventloop for PyQt.
from quamash import QEventLoop

# widgets
from base import (QApplication,  QDialog, QFrame, QHBoxLayout, HBoxLayout, QIcon, QLabel, QListWidget, QListWidgetItem,
                  QPushButton, PicLabel, QScrollArea, ScrollArea, Qt, QTabWidget, QVBoxLayout, VBoxLayout,
                  QWidget,QDesktopWidget)
from welcomeFrame import WelcomeFrame
from tfRecordMakeFrame import TFRecordMakeFrame
from resizeImagesFrame import ResizeImagesFrame

from leNet5TrainFrame import LeNet5TrainFrame
from leNet5EvlFrame import LeNet5EvlFrame
from leNet5OnePicFrame import LeNet5OnePicFrame

from resnetIv2TrainFrame import ResnetIv2TrainFrame
from resnetIv2EvlFrame import ResnetIv2EvlFrame
from resnetIv2OnePicFrame import ResnetIv2OnePicFrame

#feature
from configMainFeatures import(ConfigHeader,ConfigNavigation)
from configTFRecordMakeFeatures import ConfigTFRecordMake
from configResizeImagesFeatures import ConfigResizeImages

from configLeNet5TrainFeatures import ConfigLeNet5Train
from configLeNet5EvlFeatures import ConfigLeNet5Evl
from configLeNet5OnePicFeatures import ConfigLeNet5OnePic

from configResnetIv2TrainFeatures import ConfigResnetIv2Train
from configResnetIv2EvlFeatures import ConfigResnetIv2Evl
from configResnetIv2OnePicFeatures import ConfigResnetIv2OnePic

# 用于承载整个界面。所有窗口的父窗口，所有窗口都可以在父窗口里找到索引。
class Window(QWidget):
    """Window 承载整个界面。"""
    def __init__(self):
        super(Window, self).__init__()
        self.setObjectName('MainWindow')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("基于卷积神经网络的交通标志自动识别系统的设计与实现widow_title")

        self.resize(1000, 650)
        #头，导航，主界面
        self.header = Header(self)
        self.navigation = Navigation(self)
        self.welcomeContent = WelcomeFrame(self)
        self.tfRecordMakeContent=TFRecordMakeFrame(self)
        self.resizeImagesContent=ResizeImagesFrame(self)
        #LeNet5部分
        self.leNet5TrainContent=LeNet5TrainFrame(self)
        self.leNet5EvlContent=LeNet5EvlFrame(self)
        self.leNet5OnePicContent=LeNet5OnePicFrame(self)
        #Resnet Inception v2部分
        self.resnetIv2TrainContent=ResnetIv2TrainFrame(self)
        self.resnetIv2EvlContent=ResnetIv2EvlFrame(self)
        self.resnetIv2OnePicContent=ResnetIv2OnePicFrame(self)

        self.mainContents=QTabWidget()
        self.mainContents.tabBar().setObjectName("mainTab")
       #加载Tab设置
        self.setContents()
        # 设置布局小细线。
        self.setLines()
        # 设置布局。
        self.setLayouts()
        # 注册功能。
        self.configFeatures()

        with open('QSS/window.qss', 'r',encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        self.center()
    
    # 布局。
    def setContents(self):
        """设置tab界面。"""
        # 将需要切换的窗口做成Tab，并隐藏tabBar，这样方便切换，并且可以做前进后退功能。
        
        self.mainContents.addTab(self.welcomeContent, '')
        self.mainContents.addTab(self.resizeImagesContent,'')
        self.mainContents.addTab(self.tfRecordMakeContent, '')
        
        self.mainContents.addTab(self.leNet5TrainContent, '')
        self.mainContents.addTab(self.leNet5EvlContent, '')
        self.mainContents.addTab(self.leNet5OnePicContent, '')

        self.mainContents.addTab(self.resnetIv2TrainContent, '')
        self.mainContents.addTab(self.resnetIv2EvlContent, '')
        self.mainContents.addTab(self.resnetIv2OnePicContent, '')

        self.mainContents.setCurrentIndex(0)
        
    def setLines(self):
        """设置布局小细线。"""
        self.line1 = QFrame(self)
        self.line1.setObjectName("line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Plain)
        self.line1.setLineWidth(2)

    def setLayouts(self):

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.header)
        self.mainLayout.addWidget(self.line1)
        
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setStretch(0, 70)
        self.contentLayout.setStretch(1, 570)
        
        self.contentLayout.addWidget(self.navigation)
        self.contentLayout.addWidget(self.mainContents)

        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)   

        self.mainLayout.addLayout(self.contentLayout)
    
        self.mainLayout.setStretch(0, 43)
        self.mainLayout.setStretch(1, 0)
        self.mainLayout.setStretch(2, 600)
        
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

    
    # 注册所有功能。
    def configFeatures(self):
      #  self.config = ConfigWindow(self)
        self.header.config = ConfigHeader(self.header)
        self.navigation.config = ConfigNavigation(self.navigation)
        
        self.resizeImagesContent.config=ConfigResizeImages(self.resizeImagesContent)
        self.tfRecordMakeContent.config=ConfigTFRecordMake(self.tfRecordMakeContent)
        
        self.leNet5TrainContent.config=ConfigLeNet5Train(self.leNet5TrainContent)
        self.leNet5EvlContent.config=ConfigLeNet5Evl(self.leNet5EvlContent)
        self.leNet5OnePicContent.config=ConfigLeNet5OnePic(self.leNet5OnePicContent)
        
        self.resnetIv2TrainContent.config=ConfigResnetIv2Train(self.resnetIv2TrainContent)
        self.resnetIv2EvlContent.config=ConfigResnetIv2Evl(self.resnetIv2EvlContent)
        self.resnetIv2OnePicContent.config=ConfigResnetIv2OnePic(self.resnetIv2OnePicContent)

    
    def center(self):
        screen = QDesktopWidget().screenGeometry()  
        size = self.geometry()  
        self.move(((screen.width() - size.width()) / 5)*2,    
                  ((screen.height() - size.height()) / 5)*2)  
        

# 标题栏，包括logo，搜索，登陆，最小化/关闭。
class Header(QFrame):

    def __init__(self, parent=None):
        """头部区域，包括图标/题目/最大/小化/关闭。"""

        super(Header, self).__init__()
        self.setObjectName('Header')

        self.parent = parent

      #  self.loginBox = LoginBox(self)

        with open('QSS/header.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        # 加载按钮设置。
        self.setButtons()
        # 加载标签设置。
        self.setLabels()
        # 加载小细线装饰。
        self.setLines()
        # 加载布局设置。
        self.setLayouts()

    # 布局。
    def setButtons(self):
        """创建所有的按钮。"""

        self.closeButton = QPushButton('×', self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMinimumSize(21, 17)

        self.showminButton = QPushButton('_', self)
        self.showminButton.setObjectName("minButton")
        self.showminButton.setMinimumSize(21, 17)

        self.showmaxButton = QPushButton('□')
        self.showmaxButton.setObjectName("maxButton")
        self.showmaxButton.setMaximumSize(16, 16)


    def setLabels(self):
        """创建所需的所有标签。"""
        self.descriptionLabel = QLabel(self)
        self.descriptionLabel.setText("<b>基于卷积神经网络的交通标志自动识别系统的设计与实现</b>")


    def setLines(self):
        """设置装饰用小细线。"""
        self.line1 = QFrame(self)
        self.line1.setObjectName("line1")
        self.line1.setFrameShape(QFrame.VLine)
        self.line1.setFrameShadow(QFrame.Plain)
        self.line1.setMaximumSize(1, 25)

    def setLayouts(self):
        """设置布局。"""
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addSpacing(4)
        self.mainLayout.addWidget(self.descriptionLabel)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.line1)
        
        self.mainLayout.addSpacing(30)
        self.mainLayout.addWidget(self.showminButton)
        self.mainLayout.addWidget(self.showmaxButton)
        self.mainLayout.addSpacing(3)
        self.mainLayout.addWidget(self.closeButton)


        self.setLayout(self.mainLayout)

    # 事件。
    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.m_drag = True
            self.parent.m_DragPosition = event.globalPos()-self.parent.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.parent.move(event.globalPos()-self.parent.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = False


# 左侧的导航栏
'''如下：
|--主界面
|  |-主界面
|  |-tfRecord制作
|  |-图片尺寸重置
|--LeNet5模型
|  |-训练模型
|  |-评估模型
|  |-单图测试
|--Resnet_inception_v2模型
|  |-训练模型
|  |-评估模型
|  |-单图测试


'''
class Navigation(QScrollArea):
    def __init__(self, parent=None):

        super(Navigation, self).__init__(parent)
        self.parent = parent
        self.frame = QFrame()
        self.setMaximumWidth(200)

        self.setWidget(self.frame)
        self.setWidgetResizable(True)
        self.frame.setMinimumWidth(200)
  
        with open('QSS/navigation.qss', 'r') as f:
            style = f.read()
            self.setStyleSheet(style)
            self.frame.setStyleSheet(style)

        # 设置显示信息
        self.setLabels()
        # 设置详细的内容
        self.setListViews()

        self.setLayouts()


    # 布局。
    def setLabels(self):
        """定义所有的标签。"""
        self.mainNaviLabel = QLabel("  主界面:")
        self.mainNaviLabel.setObjectName("mainNaviLabel")
        self.mainNaviLabel.setMaximumHeight(37)
        self.mainNaviLabel.setMinimumHeight(30)
        
        self.leNet5Label = QLabel("  Le-Net5模型:")
        self.leNet5Label.setObjectName("leNet5Label")
        self.leNet5Label.setMaximumHeight(37)
        self.mainNaviLabel.setMinimumHeight(30)
        
        self.resnetIv2Label = QLabel("  Resnet_Inception_v2模型:")
        self.resnetIv2Label.setObjectName("resnetIv2Label")
        self.resnetIv2Label.setMaximumHeight(37)
        self.mainNaviLabel.setMinimumHeight(30)
        
    def setListViews(self):
        """定义承载功能的ListView"""
        """定义主界面栏"""
        self.naviMainList=QListWidget()
        self.naviMainList.setMaximumHeight(110)
        self.naviMainList.setObjectName("naviMainList")
        self.naviMainList.addItem(QListWidgetItem("主界面"))
        self.naviMainList.addItem(QListWidgetItem("重制图片尺寸"))
        self.naviMainList.addItem(QListWidgetItem("tfRecord制作"))

        
        self.naviMainList.setCurrentRow(0)
        
        self.naviLeNet5List = QListWidget()
        self.naviLeNet5List.setMaximumHeight(110)
        self.naviLeNet5List.setObjectName("naviLeNet5List")
        self.naviLeNet5List.addItem(QListWidgetItem("训练模型"))
        self.naviLeNet5List.addItem(QListWidgetItem("评估模型"))
        self.naviLeNet5List.addItem(QListWidgetItem("单图预测"))

        self.naviResnetIv2List = QListWidget()
        self.naviResnetIv2List.setMaximumHeight(310)
        self.naviResnetIv2List.setObjectName("naviResnetIv2List")
        self.naviResnetIv2List.addItem(QListWidgetItem( "训练模型"))
        self.naviResnetIv2List.addItem(QListWidgetItem( "评估模型"))
        self.naviResnetIv2List.addItem(QListWidgetItem( "单图预测"))
        
    

    def setLayouts(self):
        """定义布局。"""
        self.mainLayout = VBoxLayout(self.frame)
        self.mainLayout.addSpacing(10)
        #主界面导航
        self.mainLayout.addWidget(self.mainNaviLabel)
        self.mainLayout.addSpacing(13)
        self.mainLayout.addWidget(self.naviMainList)
        self.mainLayout.addSpacing(11)
        #LeNet5界面导航
        self.mainLayout.addWidget(self.leNet5Label)
        self.mainLayout.addSpacing(13)
        self.mainLayout.addWidget(self.naviLeNet5List)
        self.mainLayout.addSpacing(11)
        #Resnet Inception v2导航
        self.mainLayout.addWidget(self.resnetIv2Label)
        self.mainLayout.addSpacing(13)
        self.mainLayout.addWidget(self.naviResnetIv2List)
        self.mainLayout.addSpacing(11)

        self.mainLayout.addStretch(1)

        self.setContentsMargins(0, 0, 0, 0)


# 主要内容区，最初的界面，方便构建。
class MainContent(ScrollArea):
    # 定义一个滑到了最低部的信号。
    # 方便子控件得知已经滑到了最底部，要做些加载的动作。

    def __init__(self, parent=None):
        """主内容区，包括推荐歌单等。"""
        super(MainContent, self).__init__()
        self.parent = parent
        self.setObjectName("MainContent")

        # 连接导航栏的按钮。
        # self.parent.navigation.navigationListFunction = self.navigationListFunction
        with open("QSS/mainContent.qss", 'r', encoding='utf-8') as f:
            self.style = f.read()
            self.setStyleSheet(self.style)

        self.tab = QTabWidget()
        self.tab.setObjectName("contentsTab")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.tab)

        self.frame.setLayout(self.mainLayout)

    def addTab(self, widget, name=''):
        self.tab.addTab(widget, name)

    

def start():
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=Window()
    main.show()
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)
    

if __name__ == '__main__':
    start()    
