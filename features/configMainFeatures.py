# -*- coding: utf-8 -*-
from base import  QObject
#主界面功能
#标题栏注册
class ConfigHeader(QObject):
    
    def __init__(self, header):
        super(ConfigHeader, self).__init__()
        self.header = header
        
        # 用于确定是否最大化.   
        self.isMax = False
        self.bindConnect()

    def bindConnect(self):
        self.header.closeButton.clicked.connect(self.header.parent.close)
        self.header.showminButton.clicked.connect(self.header.parent.showMinimized)
        self.header.showmaxButton.clicked.connect(self.showMaxiOrRevert)
        
    def showMaxiOrRevert(self):
        if self.isMax:
            self.header.parent.showNormal()
            self.isMax = False
        else:
            self.header.parent.showMaximized()
            self.isMax = True

#导航栏注册
class ConfigNavigation(QObject):

    def __init__(self, navigation):
        super(ConfigNavigation, self).__init__()
        self.navigation = navigation
        self.mainContents = self.navigation.parent
        self.naviNumMain=0
        self.naviNumLeNet5=3
        self.naviNumResnetIv2=6
        self.bindConnect()

    def bindConnect(self):
        self.navigation.naviMainList.itemPressed.connect(self.naviMainListItemClickEvent)
        self.navigation.naviLeNet5List.itemPressed.connect(self.naviLeNet5ListItemClickEvent)
        self.navigation.naviResnetIv2List.itemPressed.connect(self.naviResnetIv2ListItemClickEvent)

    def naviMainListItemClickEvent(self):
        """主界面栏点击事件。"""
        
        self.navigation.naviLeNet5List.setCurrentRow(-1)
        self.navigation.naviResnetIv2List.setCurrentRow(-1)

        """处理事件。"""
        self.naviMainListFunction()

    def naviLeNet5ListItemClickEvent(self, item):
        """LeNet5点击事件。"""
       
        self.navigation.naviMainList.setCurrentRow(-1)
        self.navigation.naviResnetIv2List.setCurrentRow(-1)

        """处理事件。"""
        self.naviLeNet5ListFunction(item)

    def naviResnetIv2ListItemClickEvent(self, item):
        """ResnetIv2点击事件。"""
        

        self.navigation.naviMainList.setCurrentRow(-1)
        self.navigation.naviLeNet5List.setCurrentRow(-1)

        """处理事件。"""
        self.naviResnetIv2ListFunction(item)

    def naviMainListFunction(self):
        if self.navigation.naviMainList.currentRow() == 0:
            self.navigation.parent.mainContents.setCurrentIndex(self.naviNumMain+0)
        elif self.navigation.naviMainList.currentRow() == 1:
            self.navigation.parent.mainContents.setCurrentIndex(self.naviNumMain+1)
        elif self.navigation.naviMainList.currentRow() == 2:
            self.navigation.parent.mainContents.setCurrentIndex(self.naviNumMain+2)

    def naviLeNet5ListFunction(self, item):
        if self.navigation.naviLeNet5List.currentRow() == 0:
            self.mainContents.mainContents.setCurrentIndex(self.naviNumLeNet5+0)
        elif self.navigation.naviLeNet5List.currentRow() == 1:
            self.mainContents.mainContents.setCurrentIndex(self.naviNumLeNet5+1)
        elif self.navigation.naviLeNet5List.currentRow() == 2:
            self.mainContents.mainContents.setCurrentIndex(self.naviNumLeNet5+2)

    def naviResnetIv2ListFunction(self, item):
        if self.navigation.naviResnetIv2List.currentRow() == 0:
            self.mainContents.mainContents.setCurrentIndex(self.naviNumResnetIv2+0)
        elif self.navigation.naviResnetIv2List.currentRow() == 1:
            self.mainContents.mainContents.setCurrentIndex(self.naviNumResnetIv2+1)
        elif self.navigation.naviResnetIv2List.currentRow() == 2:
            self.mainContents.mainContents.setCurrentIndex(self.naviNumResnetIv2+2)

