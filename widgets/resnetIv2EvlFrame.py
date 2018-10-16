# -*- coding: utf-8 -*-
import os 
import sys
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
            os.path.join(myFolder, 'features'),os.path.join(myFolder,'resentiv2'),os.path.join(myFolder,'QSS')
] + sys.path

from base import (QApplication,QWidget)

from selfFrameBase import SelfBaseFrame
from matplotForPyqt5 import NavToolbar,PyqtMplCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from configResnetIv2EvlFeatures import ConfigResnetIv2Evl

import asyncio
from quamash import QEventLoop

#forMatlab
import random

isTestingPrint=True

# ResnetIv2评估界面
class ResnetIv2EvlFrame(SelfBaseFrame):

    def __init__(self, parent=None):
        super(ResnetIv2EvlFrame, self).__init__(parent)
        self.titleLabel.setText("resnet inception v2网络评估界面")
        self.paraWidget.paraLabel.setText("评估参数")
        self.paraWidget.runTimeForeLabel.setText("评估消耗时间 ")
        self.paraWidget.runTimeLabel.setText("0")
        self.paraWidget.numStepButton.setText("默认不可修改")
        self.paraWidget.numStepButton.setEnabled(False)
        self.paraWidget.numStepLabel.setText("5")
        self.paraWidget.changeButton.setText("开始评估")
        self.matplotWidget.welcomeLabel.setText("<b>step-accuracy图</b>")
        self.matplotWidget.baseMpl.re_figure_accuracy()
        self.matplotWidget.baseMpl.compute_initial_figure_accuracy()


if __name__ == '__main__':
    os.chdir("..")
    
    app = QApplication(sys.argv)

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)
    asyncio.set_event_loop(eventLoop)
    
    main=ResnetIv2EvlFrame()
    #  main.show()
    main.config=ConfigResnetIv2Evl(main)
#    main.matplotWidget.baseMpl.re_figure()

    main.show()
    
    
    with eventLoop:
        eventLoop.run_forever()

    sys.exit(0)

      
