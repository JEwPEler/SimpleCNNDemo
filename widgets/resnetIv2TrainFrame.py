# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'resentiv2')
] + sys.path

from base import (QApplication,QWidget)

from selfFrameBase import SelfBaseFrame

import asyncio
from quamash import QEventLoop

#forMatlab
import random

from configResnetIv2TrainFeatures import ConfigResnetIv2Train

isTestingPrint=True

# ResnetIv2训练界面

class ResnetIv2TrainFrame(SelfBaseFrame):

    def __init__(self, parent=None):
        super(ResnetIv2TrainFrame, self).__init__(parent)
        self.titleLabel.setText("ResnetIv2网络训练界面")
        self.paraWidget.runTimeForeLabel.setText("训练用时:")
        self.paraWidget.numStepButton.setText("修改训练次数")
        self.paraWidget.changeButton.setText("开始训练")
        self.paraWidget.numStepLabel.setText("2")

   



if __name__ == '__main__':
    os.chdir("..")
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=ResnetIv2TrainFrame()
    main.config=ConfigResnetIv2Train(main)
    main.show()
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)
