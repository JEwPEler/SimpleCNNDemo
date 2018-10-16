# -*- coding: utf-8 -*-

"""用于定义几个需要多次调用的基础类。"""
__author__ = 'cyrbuzz'

from queue import Queue

# 这是一个次级目录。
import os
import sys
# sys.path.append('..')
# sys.path.append('../networks')
import pickle
import hashlib
import os.path

# PEP8不允许使用通配符的原因是会混淆命名空间。
# PyQt5的所有命名都是QXXX, 这边暂时不改了。
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#from network import Requests


def checkFolder(filenames:iter):
    # /test/test/file.suffix
    for filename in filenames:
        splits = filename.split('/')
        # 检查目录是否存在.
        for i in range(len(splits[:-1])):
            dirs = '/'.join(splits[:i+1])
            if not os.path.isdir(dirs):
                os.mkdir(dirs)

        if not os.path.isfile(filename):
            with open(filename, 'wb') as f:
                pass

# 一个用于继承的类，方便多次调用。
class ScrollArea(QScrollArea):
    """包括一个ScrollArea做主体承载一个QFrame的基础类。"""
    scrollDown = pyqtSignal()

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__()
        self.parent = parent
        self.frame = QFrame()
        self.frame.setObjectName('frame')
        # 用于发出scroll滑到最底部的信号。
        self.verticalScrollBar().valueChanged.connect(self.sliderPostionEvent)

        self.setWidgetResizable(True)

        self.setWidget(self.frame)

    def sliderPostionEvent(self):
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            self.scrollDown.emit()

    def maximumValue(self):
        return self.verticalScrollBar().maximum()


# 去除了margin和spacing的布局框。
class VBoxLayout(QVBoxLayout):

    def __init__(self, *args):
        super(VBoxLayout, self).__init__(*args)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class HBoxLayout(QHBoxLayout):

    def __init__(self, *args):
        super(HBoxLayout, self).__init__(*args)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


# 默认情况下。
# ----!!!----
# 一个水平居中的布局。
class HStretchBox(HBoxLayout):

    def __init__(self, parentLayout, *widgets, frontStretch=1, behindStretch=1):
        super(HStretchBox, self).__init__()
        self.addStretch(frontStretch)
        for i in widgets:
            self.addWidget(i)

        self.addStretch(behindStretch)

        parentLayout.addLayout(self)


# 默认情况下。
#  |
#  !
#  |
# 一个垂直居中的布局。
class VStretchBox(VBoxLayout):

    def __init__(self, parentLayout, *widgets, frontStretch=1, behindStretch=1):
        super(VStretchBox, self).__init__()
        self.addStretch(frontStretch)
        for i in widgets:
            self.addWidget(i)
        self.addStretch(behindStretch)

        self.parentLayout.addLayout(self)

#处理图片
class PicLabel(QLabel):

    def __init__(self, src=None, width=200, height=200, pixMask=None):
        super(PicLabel, self).__init__()

        self.src = None

        self.width = width
        self.height = height

        self.pixMask = None
        if pixMask:
            self.pixMask = pixMask
        if src:
            self.setSrc(src)

        if self.width:
            self.setMaximumSize(self.width, self.height)
            self.setMinimumSize(self.width, self.height)

    def setSrc(self, src):
        src = str(src)
        try:
            self.src = src
            pix = QPixmap(src)
            pix.load(src)
            pix = pix.scaled(self.width, self.height)
            # mask需要与pix是相同大小。
            if self.pixMask:
                mask = QPixmap(self.pixMask)
                mask = mask.scaled(self.width, self.height)
                pix.setMask(mask.createHeuristicMask())

            self.setPixmap(pix)
        except:
            pass

    def getSrc(self):
        """返回该图片的地址。"""
        return self.src
    
def deal_time(x):
    x = str(x)
    if len(x) == 1:
        x = '0' + x

    return x

def itv2time(iItv):
    iItv = int(iItv)

    # 地板除求小时整数。
    h = iItv//3600
    # 求余数。
    h_remainder = iItv % 3600

    # 地板除求分钟整数。
    m = h_remainder // 60
    # 求余数 为秒。
    s = h_remainder % 60

    return ":".join(map(deal_time,(h,m,s)))


    
if __name__ == '__main__':
    import os
    os.chdir('..')

    app = QApplication([])

    # a = QFrame()
    a = PicLabel('resource/one_pic.jpg', width=264, height=264)
    # a.setObjectName('sss')
    # a.setStyleSheet('QLabel#sss {border-image: url(F:/pics/one.jpg);}')
    # a.resize(500, 600)
    b = PicLabel('resource/one_pic.jpg', 64, 64)
    b.setStyleSheet('QLabel {background-color: rgba(0, 0, 0,50%);}')
    c = VBoxLayout(a)
    c.addWidget(b)
    a.show()

    exit(app.exec_())
