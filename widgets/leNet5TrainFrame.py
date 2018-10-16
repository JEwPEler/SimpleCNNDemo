# -*- coding: utf-8 -*-

import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path

from base import (QApplication,QWidget)

from selfFrameBase import SelfBaseFrame

from configLeNet5TrainFeatures import ConfigLeNet5Train

import asyncio
from quamash import QEventLoop

#forMatlab
import random

isTestingPrint=True

# LeNet5训练界面
class LeNet5TrainFrame(SelfBaseFrame):

    def __init__(self, parent=None):
        super(LeNet5TrainFrame, self).__init__(parent)
        self.titleLabel.setText("leNet5网络训练界面")
        self.paraWidget.runTimeForeLabel.setText("训练用时:")
        self.paraWidget.numStepButton.setText("修改训练次数")
        self.paraWidget.changeButton.setText("开始训练")
        self.paraWidget.numStepLabel.setText("50")

   


if __name__ == '__main__':
    os.chdir("..")
    
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=LeNet5TrainFrame()
    #  main.show()
    main.config=ConfigLeNet5Train(main)
#    main.matplotWidget.baseMpl.re_figure()

    main.show()
    
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)
