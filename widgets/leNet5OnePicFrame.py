# -*- coding: utf-8 -*-

"""LeNet5单图预测界面"""
from base import (QApplication,QCursor,QWidget, QFrame, Qt, QTabWidget, QTextEdit,  QLabel, QIcon, QPushButton, QHBoxLayout, QVBoxLayout, 
                                     QGridLayout, QTableWidgetItem, PicLabel, ScrollArea, VBoxLayout, HBoxLayout, pyqtSignal)
import os 
import sys
import asyncio
from quamash import QEventLoop

myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path
from onePicFrameBase import OnePicFrameBase
from configLeNet5OnePicFeatures import ConfigLeNet5OnePic

class LeNet5OnePicFrame(OnePicFrameBase):

    def __init__(self, parent=None):
        super(LeNet5OnePicFrame, self).__init__(parent)
        self.titleLabel.setText("leNet5单图预测：")
        
            
if __name__ == '__main__':
    os.chdir("..")
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=LeNet5OnePicFrame()
    main.config=ConfigLeNet5OnePic(main)
    main.titleLabel.setText("LeNet单图预测")
   
    main.show()
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)

 
