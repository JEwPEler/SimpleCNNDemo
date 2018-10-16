# -*- coding: utf-8 -*-

# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Downloads and converts Flowers data to TFRecords of TF-Example protos.

This module downloads the Flowers data, uncompresses it, reads the files
that make up the Flowers data and creates two TFRecord datasets: one for train
and one for test. Each TFRecord dataset is comprised of a set of TF-Example
protocol buffers, each of which contain a single image and label.

The script should take about a minute to run.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
"""
Ignore above,I have change it to make self tfRecords
"""


import math
import os
import random
import sys
import time
import tensorflow as tf


myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'lenet5')
] + sys.path
from base import ( QThread,pyqtSignal, QApplication,QWidget)


import dataset_utils

# The URL where the Traffic_Signs data can be downloaded.
#_DATA_URL = 'http://download.tensorflow.org/example_images/traffic_sign_photos.tgz'
#_DATA_URL ='F:\\pelfiles\\workstation\\python\\pycode\\dataset_pre\\for_tfrecord\\traffic_signs\\traffic_sign.rar'
# The number of images in the validation set.
_NUM_VALIDATION = 100

# Seed for repeatability.
_RANDOM_SEED = 0

# The number of shards per dataset split.
_NUM_SHARDS = 5

default_save_dir='D:\\models-master\\research\\slim\\flowers_5'
dataset_stay_dir='D:\\models-master\\research\\slim\\flowers_5\\flower_photos'

class ImageReader(object):
  """Helper class that provides TensorFlow image coding utilities."""

  def __init__(self):
    # Initializes function that decodes RGB JPEG data.
    self._decode_jpeg_data = tf.placeholder(dtype=tf.string)
    self._decode_jpeg = tf.image.decode_jpeg(self._decode_jpeg_data, channels=3)

  def read_image_dims(self, sess, image_data):
    image = self.decode_jpeg(sess, image_data)
    return image.shape[0], image.shape[1]

  def decode_jpeg(self, sess, image_data):
    image = sess.run(self._decode_jpeg,
                     feed_dict={self._decode_jpeg_data: image_data})
    assert len(image.shape) == 3
    assert image.shape[2] == 3
    return image



class TFRecordMakeThread(QThread):

  finishedSin = pyqtSignal(str)
  runningSin=pyqtSignal(str)
  def __init__(self,parent=None):
    super(TFRecordMakeThread,self).__init__()

    self.parent=None
    self.tfrecord_save_dir=default_save_dir
    self.dataset_stay_dir=dataset_stay_dir
    self.num_vali=_NUM_VALIDATION
    self.num_shards=_NUM_SHARDS

  def setSaveDir(self,save_dir):
    self.tfrecord_save_dir=save_dir
    
  def setDataDir(self,data_dir):
    self.dataset_stay_dir=data_dir

  def setNumVali(self,num_vali):
    self.num_vali=num_vali

  def setNumShards(self,num_shards):
    self.num_shards=num_shards

  def dataset_exist(self,dataset_dir):
    for split_name in ['train', 'validation']:
      for shard_id in range(self.num_shards):
        output_filename = self.get_dataset_filename(
            dataset_dir, split_name, shard_id)
        if not tf.gfile.Exists(output_filename):
          return False
    return True
  
  def run(self):
    if not tf.gfile.Exists(self.tfrecord_save_dir):
      tf.gfile.MakeDirs(self.tfrecord_save_dir)

    if self.dataset_exist(self.tfrecord_save_dir):
      print('Dataset files already exist. Exiting without re-creating them.')
      return
    photo_filenames, class_names = self.get_filenames_and_classes(self.dataset_stay_dir)
    class_names_to_ids = dict(zip(class_names, range(len(class_names))))
    random.seed(_RANDOM_SEED)
    random.shuffle(photo_filenames)
    training_filenames = photo_filenames[self.num_vali:]
    validation_filenames = photo_filenames[:self.num_vali]
    self.convert_dataset('train', training_filenames, class_names_to_ids,
                     self.tfrecord_save_dir)
    self.convert_dataset('validation', validation_filenames, class_names_to_ids,
                     self.tfrecord_save_dir)
    labels_to_class_names = dict(zip(range(len(class_names)), class_names))
    dataset_utils.write_label_file(labels_to_class_names, self.tfrecord_save_dir)
    print('\nFinished converting the Traffic_Signs dataset!')
    self.finished_str='Finished converting the Traffic_Signs dataset!'
    self.finishedSin.emit(self.finished_str)


  def get_filenames_and_classes(self,dataset_stay_dir):
    #dataset_stay_root = os.path.join(dataset_dir, 'traffic_sign_photos')
    dataset_stay_root = dataset_stay_dir
    directories = []
    class_names = []
    for filename in os.listdir(dataset_stay_root):
      path = os.path.join(dataset_stay_root, filename)
      if os.path.isdir(path):
        directories.append(path)
        class_names.append(filename)

    photo_filenames = []
    for directory in directories:
      for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        photo_filenames.append(path)

    return photo_filenames, sorted(class_names)


  def get_dataset_filename(self,dataset_stay_dir, split_name, shard_id):
    fore_filename=os.path.split(os.path.realpath(dataset_stay_dir))[1]
    output_filename = '%s_%s_%05d-of-%05d.tfrecord' % (
        fore_filename,split_name, shard_id, self.num_shards)
    return os.path.join(self.tfrecord_save_dir, output_filename)




  def convert_dataset(self,split_name, filenames, class_names_to_ids, dataset_dir):
    assert split_name in ['train', 'validation']

    num_per_shard = int(math.ceil(len(filenames) / float(self.num_shards)))

    with tf.Graph().as_default():
      image_reader = ImageReader()

      with tf.Session('') as sess:

        for shard_id in range(self.num_shards):
          output_filename = self.get_dataset_filename(
              self.dataset_stay_dir, split_name, shard_id)

          with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
            start_ndx = shard_id * num_per_shard
            end_ndx = min((shard_id+1) * num_per_shard, len(filenames))
            for i in range(start_ndx, end_ndx):
              sys.stdout.write('\r>> Converting image %d/%d shard %d' % (
                  i+1, len(filenames), shard_id))
              self.running_str=' Converting image %d/%d shard %d' % (
                  i+1, len(filenames), shard_id)
              self.runningSin.emit(self.running_str)
              sys.stdout.flush()

              # Read the filename:
              image_data = tf.gfile.FastGFile(filenames[i], 'rb').read()
              height, width = image_reader.read_image_dims(sess, image_data)

              class_name = os.path.basename(os.path.dirname(filenames[i]))
              class_id = class_names_to_ids[class_name]

              example = dataset_utils.image_to_tfexample(
                  image_data, b'jpg', height, width, class_id)
              tfrecord_writer.write(example.SerializeToString())

    sys.stdout.write('\n')
    sys.stdout.flush()



class Main(QWidget):  
  def __init__(self, parent = None):  
    super(Main,self).__init__(parent)
    print('main start!please wait')
    self_start_time = time.time()
    run_str='F:\\pelfiles\\workstation\\python\\pycode\\gradu\\self\\try_cod\\try_7_test_multi_threath\\TrafficSignsClassicy\\utils'
    stay_str='D:\\models-master\\research\\slim\\traffic\\traffic_sign_photos'
    ##创建一个线程实例并设置名称、变量、信号槽  
    self.thread =TFRecordMakeThread(self)
    self.thread.setSaveDir(run_str)
    self.thread.setDataDir(stay_str)
    self.thread.setNumVali(50)
    self.thread.setNumShards(2)

    self.thread.start()
    print("this is a return")

    self_end_time=time.time()
    print("total use:",self_end_time-self_start_time)
  
     

        
if __name__ == "__main__":
  app = QApplication([])  
  
  main = Main()  
  main.show()  
  
  app.exec_()  
   


                
