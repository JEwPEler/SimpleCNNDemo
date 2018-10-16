# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow.python.platform import tf_logging as logging
from tensorflow.contrib.framework.python.ops.variables import get_or_create_global_step
import inception_preprocessing
from inception_resnet_v2 import inception_resnet_v2, inception_resnet_v2_arg_scope
import time
import os
import sys
from resnetIv2TrainThread import get_split, load_batch
myFolder = os.path.split(os.path.dirname(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'features'),os.path.join(myFolder,'resnetiv2')
] + sys.path
from base import ( QThread,pyqtSignal, QApplication,QWidget)

import matplotlib.pyplot as plt
plt.style.use('ggplot')

isTestSelf=True

slim = tf.contrib.slim

#State your log directory where you can retrieve your model
thisFolder = os.path.split(os.path.realpath(__file__))[0]

log_dir = os.path.join(thisFolder,  "log")
#log_dir = './log'
#Create a new evaluation log directory to visualize the validation process

log_eval =os.path.join(thisFolder,  'log_eval_test')
#log_eval = './log_eval_test'
#State the dataset directory where the validation set is found
dataset_dir = os.path.join(thisFolder,  "dataset")
#dataset_dir = './dataset'
#State the batch_size to evaluate each time, which can be a lot more than the training batch
batch_size = 36

#State the number of epochs to evaluate
num_epochs = 5

num_steps = 5 

#Get the latest checkpoint file
checkpoint_file = tf.train.latest_checkpoint(log_dir)

class ResnetIv2EvlThread(QThread):
    
    oneEvlOverSin = pyqtSignal(dict)
    finishedEvlSin = pyqtSignal()  
    runningSin=pyqtSignal(str)
    def __init__(self,parent=None):
        super(ResnetIv2EvlThread,self).__init__()
        self.parent=parent

    def run(self):
       
        if not os.path.exists(log_eval):
            os.mkdir(log_eval)

    
        with tf.Graph().as_default() as graph:
            tf.logging.set_verbosity(tf.logging.INFO)
            dataset = get_split('validation', dataset_dir)
            images, raw_images, labels = load_batch(dataset, batch_size = batch_size, is_training = True)
            num_batches_per_epoch = dataset.num_samples / batch_size
            num_steps_per_epoch = num_batches_per_epoch

            with slim.arg_scope(inception_resnet_v2_arg_scope()):
                logits, end_points = inception_resnet_v2(images, num_classes = dataset.num_classes, is_training = True)

          
            variables_to_restore = slim.get_variables_to_restore()
            saver = tf.train.Saver(variables_to_restore)
            def restore_fn(sess):
                return saver.restore(sess, checkpoint_file)

            predictions = tf.argmax(end_points['Predictions'], 1)
            accuracy, accuracy_update = tf.contrib.metrics.streaming_accuracy(predictions, labels)
            metrics_op = tf.group(accuracy_update)
           
            global_step = get_or_create_global_step()
            global_step_op = tf.assign(global_step, global_step + 1)            

            def eval_step(sess, metrics_op, global_step):
                '''
                Simply takes in a session, runs the metrics op and some logging information.
                '''
                start_time = time.time()
                _, global_step_count, accuracy_value = sess.run([metrics_op, global_step_op, accuracy])
                time_elapsed = time.time() - start_time

                #Log some information
                logging.info('Global Step %s: Streaming Accuracy: %.4f (%.2f sec/step)', global_step_count, accuracy_value, time_elapsed)
                self.out_message='Global Step %s: Streaming Accuracy: %.4f (%.2f sec/step)'%(global_step_count, accuracy_value, time_elapsed)
                self.oneEvlOverSin.emit({"step":global_step_count,"accuracy_score":accuracy_value,"message":self.out_message})
                return accuracy_value


            #Define some scalar quantities to monitor
            tf.summary.scalar('Validation_Accuracy', accuracy)
            my_summary_op = tf.summary.merge_all()

            #Get your supervisor
            sv = tf.train.Supervisor(logdir = log_eval, summary_op = None, saver = None, init_fn = restore_fn)

            #Now we are ready to run in one session
            with sv.managed_session() as sess:
                for step in range(num_steps):
                    sess.run(sv.global_step)
                    #print vital information every start of the epoch as always
                    if step % num_steps == 0:
                        logging.info('Epoch: %s/%s', step / num_batches_per_epoch + 1, num_epochs)
                        log_info='Epoch: %s/%s'%( step / num_batches_per_epoch + 1, num_epochs)
                        self.runningSin.emit(log_info)
                        logging.info('Current Streaming Accuracy: %.4f', sess.run(accuracy))
                        log_info='Current Streaming Accuracy: %.4f'%( sess.run(accuracy))
                        self.runningSin.emit(log_info)
                    #Compute summaries every 10 steps and continue evaluating
                    if step % 10 == 0:
                        eval_step(sess, metrics_op = metrics_op, global_step = sv.global_step)
                        summaries = sess.run(my_summary_op)
                        sv.summary_computed(sess, summaries)
                        

                    #Otherwise just run as per normal
                    else:
                        eval_step(sess, metrics_op = metrics_op, global_step = sv.global_step)

                #At the end of all the evaluation, show the final accuracy
                logging.info('Final Streaming Accuracy: %.4f', sess.run(accuracy))

                log_info='Final Streaming Accuracy: %.4f'%(sess.run(accuracy))
                self.runningSin.emit(log_info)
                #Now we want to visualize the last batch's images just to see what our model has predicted
                raw_images, labels, predictions = sess.run([raw_images, labels, predictions])
                
                logging.info('Model evaluation has completed! Visit TensorBoard for more information regarding your evaluation.')
                log_info=('Model evaluation has completed! Visit TensorBoard for more information regarding your evaluation.')
                self.runningSin.emit(log_info)
                
                self.finishedEvlSin .emit()
                self.exit()

class Main(QWidget):  
    def __init__(self, parent = None):  
        super(Main,self).__init__(parent)  
  
        ##创建一个线程实例并设置名称、变量、信号槽  
        self.thread = ResnetIv2EvlThread(self)
        self.thread.start()
        print("this is a return")
        if isTestSelf:
            print(sys.path)


        
if __name__ == "__main__":
    app = QApplication([])  
  
    main = Main()  
    main.show()  
  
    app.exec_()  
    print('main start!please wait')
    self_start_time = time.time()
    self_end_time=time.time()
    print("total use:",self_end_time-self_start_time)
