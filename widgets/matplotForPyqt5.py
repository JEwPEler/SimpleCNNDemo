import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


# customize navigation toolbar
class NavToolbar(NavigationToolbar):
    toolitems = [('Save', 'Save the figure', 'filesave', 'save_figure')]


class PyqtMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100, title='title'):
        self.title = title
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.suptitle(title)

        # default set True ,wille False will not be able to make two line
       # self.axes.hold(True)

        self.compute_initial_figure()


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(PyqtMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        self.axes.set_ylabel('label1')
        self.axes.set_xlabel('label')
        self.axes.grid(True)
        #self.axes.set_ylim(0, 0.5)


class MyDynamicMplCanvas(PyqtMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        PyqtMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1)

    def compute_initial_figure(self):
        self.xList=[0]
        self.yList=[0]
        self.zList=[0]
        self.xNum=1
        self.axes.set_ylabel('labely;labelz')
        self.axes.set_xlabel('labelx')
        self.axes.plot(self.xList,self.yList,'r',label='labely')
        self.axes.plot(self.xList,self.zList,'b',label='labelz',linestyle='--')
        
        self.axes.grid(True)

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        self.xList.append(self.xNum)
        self.xNum+=1
        self.yList.append(random.random())
        self.axes.plot(self.xList,self.yList,'r',label='labely')
        self.zList.append(random.random())
        self.axes.plot(self.xList,self.zList,'b',label='labelz',linestyle='--')

        self.axes.grid(True)
        self.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100, title='Title 2')
        dcntb = NavigationToolbar(dc, self.main_widget) # full toolbar
        
        l.addWidget(dc)
        l.addWidget(dcntb)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        self.statusBar().showMessage("All hail matplotlib!", 2000)


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About",
  """embedding_in_qt5.py example
  Copyright 2015 BoxControL

  This program is a simple example of a Qt5 application embedding matplotlib
  canvases. It is base on example from matplolib documentation, and initially was
  developed from Florent Rougon and Darren Dale.

  http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html

  It may be used and modified with no restriction; raw copies as well as
  modified versions may be distributed without limitation.""")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("Pyqt5 Matplot Example")
    aw.show()
    #sys.exit(qApp.exec_())
    app.exec_()
