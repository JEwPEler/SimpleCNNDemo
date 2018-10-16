# -*- coding: utf-8 -*-

from PIL import Image
import os
import sys
import glob
import time
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path
from base import ( QThread,pyqtSignal, QApplication,QWidget)

isTestSelf=True

thisFolder = os.path.split(os.path.realpath(__file__))[0]

#图片尺寸重置功能实现
class ResizeImagesThread(QThread):

    runningSin=pyqtSignal(str)
    finishedSin=pyqtSignal(str)

    def __init__(self,parent=None):
        super(ResizeImagesThread,self).__init__()
        self.parent=parent
        self.resize_width=32
        self.resize_height=32
        self.save_dir=None
        self.data_dir=None

    def setResizeWidth(self,width):
        self.resize_width=width

    def setResizeHeight(self,height):
        self.resize_height=height
        
    def setSaveDir(self,save_dir):
        self.save_dir=save_dir
    
    def setDataDir(self,data_dir):
        self.data_dir=data_dir

    def run(self):
        if isTestSelf:
            print("run start")

        sub_dirs = [x[0] for x in os.walk(self.data_dir)]
        if isTestSelf:
            print("sub_dirs over.")
        for sub_dir in sub_dirs[1:]:
            file_glob = os.path.join(sub_dir, "*.*")
            files = glob.glob(file_glob)
            for file in files:
                if isTestSelf:
                    print("oldfile:",file)
                try:
                    img = Image.open(file)
                    img = img.resize((self.resize_width,self.resize_height))
                    new_file=file.split(self.data_dir)[1]
                    new_path=self.save_dir+new_file
                    new_dir=os.path.dirname(new_path)
                    if isTestSelf:
                        print("new_file:",new_file)
                        print("new_path:",new_path)
                        print("new_dir_:",new_dir)

                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)

                    img.save(new_path)
                    self.runningSin.emit(new_file)
                except:
                    pass
                
        self.finishedSin.emit("重置完毕")
        if isTestSelf:
            print("savedir",self.save_dir)
            print("datadir",self.data_dir)
            print("end over.")
class Main(QWidget):  
  def __init__(self, parent = None):  
    super(Main,self).__init__(parent)
    print('main start!please wait')
    self_start_time = time.time()
    run_str='F:\\pelfiles\\workstation\\python\\pycode\\gradu\\self\\try_cod\\try_7_test_multi_threath\\TrafficSignsClassicy\\cache'
    stay_str='F:\\pelfiles\\workstation\\python\\pycode\\gradu\\self\\try_cod\\try_7_test_multi_threath\\temppys\\data32'
    ##创建一个线程实例并设置名称、变量、信号槽  
    self.thread =ResizeImagesThread(self)
    self.thread.setSaveDir(run_str)
    self.thread.setDataDir(stay_str)
    self.thread.setResizeWidth(448)
    self.thread.setResizeHeight(448)

    self.thread.start()
    print("this is a return")

    self_end_time=time.time()
    print("total use:",self_end_time-self_start_time)
  
     

        
if __name__ == "__main__":
  app = QApplication([])  
  
  main = Main()  
  main.show()  
  
  app.exec_()  
   


                
