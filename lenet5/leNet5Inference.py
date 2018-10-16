# -*- coding: utf-8 -*-

'''
定义神经网络模型
'''
import tensorflow as tf

INPUT_NODE = 3072
OUTPUT_NODE = 8

IMAGE_SIZE = 32
NUM_CHANNELS = 3
NUM_LABELS = 8

CONV1_DEEP = 32
CONV1_SIZE = 5

CONV2_DEEP = 64
CONV2_SIZE = 5

CONV3_DEEP = 128
CONV3_SIZE = 5

FC_SIZE = 512

def create_cnn_layer(input_tensor, name, ksize, input_deep, output_deep):
    '''
    创建一层卷积层
    :param input_tensor:输入向量
    :param name: 卷积层名称
    :param ksize: 卷积核大小
    :param input_deep: 输入向量深度
    :param output_deep: 输出向量深度
    :return: 完成卷积后的向量
    '''
    with tf.variable_scope(name):
        conv_weights = tf.get_variable(
            "weight",
            [ksize, ksize, input_deep, output_deep],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        conv_biases = tf.get_variable(
            "biases",
            [output_deep],
            initializer=tf.constant_initializer(0.0)
        )
        conv = tf.nn.conv2d(
            input_tensor,
            conv_weights,
            strides=[1, 1, 1, 1],
            padding="SAME"
        )
        output_tensor = tf.nn.relu(tf.nn.bias_add(conv, conv_biases))
    return output_tensor

def create_full_layer(input_tensor, name, input_size,
                      output_size, regularizer, keep_proc, activation):
    '''
    创建一层全连接层
    :param input_tensor:输入向量
    :param name: 全连接层名称
    :param input_size: 输入向量长度
    :param output_size: 输出向量长度
    :param regularizer: 正则化函数
    :param keep_proc: dropout参数
    :param activation: 激活函数
    :return: 输出向量
    '''
    with tf.variable_scope(name):
        weights = tf.get_variable(
            "weight",
            [input_size, output_size],
            initializer=tf.truncated_normal_initializer(stddev=0.1)
        )
        if regularizer != None:
            tf.add_to_collection("losses", regularizer(weights))
        biases = tf.get_variable(
            "biases",
            [output_size],
            initializer=tf.constant_initializer(0.1)
        )
        wx_add_b = tf.matmul(input_tensor, weights) + biases
        wx_add_b = tf.nn.dropout(wx_add_b, keep_proc)
        if activation != None:
            output_tensor = activation(wx_add_b)
        else:
            output_tensor = wx_add_b
    return output_tensor

def inference_cnn(input_tensor, regularizer=None, keep_proc=1.0):
    '''
    神经网络模型，前向传播过程，采用LeNet-5模型
    :param input_tensor:输入向量
    :param regularizer:正则化函数
    :param keep_proc:dropout参数
    :return:softmax后的结果向量
    '''
    #卷积层
    conv1 = create_cnn_layer(
        input_tensor,
        "layer1-conv1",
        CONV1_SIZE,
        NUM_CHANNELS,
        CONV1_DEEP
    )
    #池化层
    with tf.name_scope("layer2-pool1"):
        pool1 = tf.nn.avg_pool(
            conv1,
            ksize=[1, 2, 2, 1],
            strides=[1, 2, 2, 1],
            padding="SAME"
        )
    #卷积层
    conv2 = create_cnn_layer(
        pool1,
        "layer3-conv2",
        CONV2_SIZE,
        CONV1_DEEP,
        CONV2_DEEP
    )
    #池化层
    with tf.name_scope("layer4-pool2"):
        pool2 = tf.nn.avg_pool(
            conv2,
            ksize=[1, 2, 2, 1],
            strides=[1, 2, 2, 1],
            padding="SAME"
        )
    '''conv3 = create_cnn_layer(
        pool2,
        "conv3",
        CONV3_SIZE,
        CONV2_DEEP,
        CONV3_DEEP
    )
    with tf.name_scope("pool3"):
        pool3 = tf.nn.max_pool(
            conv3,
            ksize=[1, 2, 2, 1],
            strides=[1, 2, 2, 1],
            padding="SAME"
        )'''
    #将向量拉伸为一维向量作为全连接层输入
    pool_shape = pool2.get_shape().as_list()
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
    reshaped = tf.reshape(pool2, [-1, nodes])
    #全连接层
    fc1 = create_full_layer(
        reshaped,
        "layer5-fc1",
        nodes,
        FC_SIZE,
        regularizer,
        keep_proc,
        tf.nn.relu
    )
    #全连接层
    fc2 = create_full_layer(
        fc1,
        "layer6-fc2",
        FC_SIZE,
        NUM_LABELS,
        regularizer,
        1.0,
        tf.nn.softmax
    )
    return fc2
