# -*- coding: utf-8 -*-
from base import (QApplication,QCursor,QWidget, QFrame, Qt, QTabWidget, QTextEdit,  QLabel, QIcon, QPushButton,  QInputDialog,QHBoxLayout, QVBoxLayout, 
                                     QGridLayout, QTableWidgetItem, PicLabel, ScrollArea, VBoxLayout, HBoxLayout, pyqtSignal)
import os 
import sys
import asyncio
from quamash import QEventLoop
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features')
] + sys.path
#forMatlab
import random
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotForPyqt5 import NavToolbar,PyqtMplCanvas

isTestingPrint=True

#slefBase界面，用于继承
class SelfBaseFrame(ScrollArea):

    def __init__(self, parent=None):
        super(SelfBaseFrame, self).__init__()

        # self.hide()
        self.parent = parent
        self.setObjectName('selfBaseFrame')
        with open('QSS/selfBaseFrame.qss', 'r', encoding='utf-8') as f:
            self.style=f.read()
            self.setStyleSheet(self.style)
        self.paraWidget=BaseParaWidget(self)
        self.matplotWidget=BaseMatplotWidget(self)

        self.initUI()
        
    def initUI(self):
        self.setLabels()
        self.setTabs()
        self.setLines()
        self.setLayouts()

    # 布局。
    def setLabels(self):

        self.titleLabel = QLabel(self.frame)
        self.titleLabel.setObjectName('titleLabel')
        self.titleLabel.setText("Base网络训练界面")
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setMaximumHeight(27)

    def setTabs(self):
        self.contentsTab = QTabWidget(self.frame)

        self.disDetailsText = QTextEdit(self.frame)
        self.disDetailsText.setReadOnly(True)
        self.disDetailsText.setObjectName('disDetailsText')
        self.disDetailsText.setMaximumWidth(1000)
        self.disDetailsText.setMaximumHeight(500)
        self.disDetailsText.setMinimumHeight(100)

        self.contentsTab.addTab(self.disDetailsText, "详细训练信息")
        
    def setLines(self):
        """设置布局小细线。"""
        self.line1 = QFrame(self)
        self.line1.setObjectName("line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Plain)
        self.line1.setLineWidth(3)

    def setLayouts(self):
        self.mainLayout = VBoxLayout()
        #训练页标题
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addSpacing(1)
        self.mainLayout.addWidget(self.line1)

        #参数调整与绘图
        self.contentLayout=HBoxLayout()

        self.contentLayout.setSpacing(3)
        self.contentLayout.addWidget(self.paraWidget)
        self.contentLayout.addWidget(self.matplotWidget)
        self.contentLayout.addSpacing(3)
        self.contentLayout.setStretch(0,30)

        self.contentLayout.setStretch(1,50)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)   


        self.mainLayout.addLayout(self.contentLayout)
        #训练详细信息
        self.mainLayout.addWidget(self.contentsTab)

        self.mainLayout.setStretch(0, 34)
        self.mainLayout.setStretch(1, 0)
        self.mainLayout.setStretch(2, 500)
        self.mainLayout.setStretch(3, 500)

        self.frame.setLayout(self.mainLayout)

"""
基础参数修改

"""
class BaseParaWidget(ScrollArea):
    def __init__(self,parent=None):
        super(BaseParaWidget, self).__init__()
        self.setObjectName('baseParaWidget')
        self.isRunningThread=False
        self.setLabels()
        self.setButtons()
        self.setLayouts()
        
    def setLabels(self):
        """创建所需的所有标签。"""
        self.paraLabel =QLabel('参数设置')
        self.paraLabel.setObjectName("paraLabel")
        self.paraLabel.setMaximumWidth(200)
        self.paraLabel.setMinimumWidth(30)
        self.paraLabel.setMaximumHeight(37)
        self.paraLabel.setObjectName('paraLabel')
        
        self.numStepForeLabel = QLabel('训练次数（step):')
        self.numStepForeLabel.setObjectName("numStepForeLabel")
        self.numStepForeLabel.setMaximumWidth(170)
        self.numStepForeLabel.setMinimumWidth(30)

        self.numStepLabel = QLabel('2')
        self.numStepLabel.setObjectName("numStepLabel")
        self.numStepLabel.setMaximumWidth(170)
        self.numStepLabel.setMinimumWidth(30)
        self.numStepLabel.setMaximumHeight(37)
        
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

        if isTestingPrint:
            print("setLabel is over!")

    def setButtons(self):
        self.numStepButton = QPushButton("修改步数")
        self.numStepButton.setObjectName('numStepButton')
        self.numStepButton.setMaximumSize(90, 24)

        self.changeButton = QPushButton(self)
        self.changeButton.setObjectName('changeButton')
        if not self.isRunningThread:
            self.changeButton.setText("开始")
        elif self.isRunningThread:
            self.changeButton.setText("停止")
        self.changeButton.setMaximumSize(90, 24)

    def setLayouts(self):
        """设置布局。"""
        self.mainLayout = VBoxLayout()
        self.mainLayout.addWidget(self.paraLabel)
        self.mainLayout.setSpacing(0)

        self.numStepLayout=HBoxLayout()
        self.numStepLayout.setSpacing(0)
        self.numStepLayout.addWidget(self.numStepForeLabel)
        self.numStepLayout.addWidget(self.numStepLabel)
        self.numStepLayout.addWidget(self.numStepButton)


        self.mainLayout.addLayout(self.numStepLayout)

        self.runTimeLayout=HBoxLayout()
        self.runTimeLayout.setSpacing(0)
        self.runTimeLayout.addWidget(self.runTimeForeLabel)
        self.runTimeLayout.addWidget(self.runTimeLabel)
        self.runTimeLayout.addWidget(self.changeButton)

        self.mainLayout.addLayout(self.runTimeLayout)

        self.mainLayout.addStretch(1)
        
        self.mainLayout.setStretch(0, 35)
        self.mainLayout.setStretch(1,35)
        self.mainLayout.setStretch(2,200)
        
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.frame.setLayout(self.mainLayout)
        

"""
matplot绘图，
"""
class BaseMatplotWidget(ScrollArea):
    def __init__(self, parent=None):
        super(BaseMatplotWidget, self).__init__()        
        self.parent = parent

        self.setLabels()
        self.setBaseMplWidget()
        self.setLayouts()
        
    def setLabels(self):
        """创建所需的所有标签。"""

        self.welcomeLabel = QLabel(self)
        self.welcomeLabel.setText("<b>step-loss图</b>")
        self.welcomeLabel.setMaximumWidth(200)
        self.welcomeLabel.setMinimumWidth(5)
        self.welcomeLabel.setMaximumHeight(37)

        
    def setBaseMplWidget(self):

        self.baseMpl=BaseMplCanvas(self, width=5, height=4, dpi=100, title='')
        self.baseMpltb = NavigationToolbar(self.baseMpl,self)

    def setMplWidget(self,mplWidget):
        self.baseMpl=mplWidget
        self.setLayout(self.mainLayout)
        
    def setLayouts(self):
        """设置布局。"""
        self.mainLayout = VBoxLayout()
        self.mainLayout.setSpacing(2)
        self.mainLayout.addWidget(self.welcomeLabel)
        self.mainLayout.addWidget(self.baseMpl)
        self.mainLayout.addWidget(self.baseMpltb)
        self.mainLayout.setStretch(0, 34)
        self.mainLayout.setStretch(1,200)
        self.mainLayout.setStretch(2,20)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.frame.setLayout(self.mainLayout)

"""
matplot绘图类,绘制step-loss图
"""
class BaseMplCanvas(PyqtMplCanvas):
    
    def __init__(self, *args, **kwargs):
        PyqtMplCanvas.__init__(self, *args, **kwargs)

    def re_figure(self):
        self.axes.set_ylabel('lossLabel')
        self.axes.set_xlabel('stepLabel')
        self.axes.cla()
        self.stepList=[]
        self.lossList=[]
        
    def re_figure_accuracy(self):
        self.stepList=[]
        self.accuracyList=[]
        self.axes.cla()
        
    def compute_initial_figure(self):
        self.stepList = arange(0.0, 3.0, 0.01)
        self.lossList = self.stepList*self.stepList
        
        self.axes.plot(self.stepList, self.lossList)
        self.axes.set_ylabel('lossLabel')
        self.axes.set_xlabel('stepLabel')
        self.axes.grid(True)

    def compute_initial_figure_accuracy(self):
        self.stepList = [1,2,3,4,5,6,7,8,9,10]
        self.accuracyList = [2,3,5,1,5,2,6,2,34,1]
        
        self.axes.plot(self.stepList, self.accuracyList)
        self.axes.set_ylabel('accuracyLabel')
        self.axes.set_xlabel('stepLabel')
        self.axes.grid(True)


    def update_figure(self,dict):
       
        self.stepList.append(dict['step'])
        self.lossList.append(dict['loss'])
        self.axes.set_ylabel('lossLabel')
        self.axes.set_xlabel('stepLabel')
        self.axes.plot(self.stepList,self.lossList,'r',label='lossLabel')

        self.axes.grid(True)
        self.draw()
        
    def update_figure_accuracy(self,dict):
        self.stepList.append(dict['step'])
        self.accuracyList.append(dict['accuracy_score']*100)
        self.axes.set_ylabel('accuracyLabel')
        self.axes.set_xlabel('stepLabel')
        self.axes.plot(self.stepList,self.accuracyList,'r',label='accuracyLabel')

        self.axes.grid(True)
        self.draw()


if __name__ == '__main__':
    os.chdir("..")
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=SelfBaseFrame()
    main.matplotWidget.baseMpl.re_figure()
    for i in range(100):
        main.matplotWidget.baseMpl.update_figure({"step":i,"loss":random.randint(0,99)})
    main.show()
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)
