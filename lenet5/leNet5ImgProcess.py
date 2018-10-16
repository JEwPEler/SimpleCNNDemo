# -*- coding: utf-8 -*-


'''
对图像数据进行划分和处理
'''
import leNet5Inference
import numpy as np
from PIL import Image
import os
import glob

thisFolder = os.path.split(os.path.realpath(__file__))[0]
TRAINING_DATA_DIR =os.path.join(thisFolder, "./data32/Training/")
TEST_DATA_DIR =os.path.join(thisFolder, "./data32/Testing/")

VALIDATION_PERCENTAGE = 10

isTestSelfTrain=False
isTestSelfEvl=True
def create_image_lists():
    '''
    对所配置的目录下的图像文件根据目录名分类，并划分成训练集、验证集和测试集
    :return: 嵌套的dict，第一层key代表数据标签，第二层key代表不同的集合
    eg:{1:{"dir":"...","training":[...],"validation":[...],"testing":[]}
        2:{...}
        ...}
    '''
    result = {}
    #训练集和验证集
    sub_dirs = [x[0] for x in os.walk(TRAINING_DATA_DIR)]
    if isTestSelfTrain:
        print(sub_dirs)
    for sub_dir in sub_dirs[1:]:
        file_list = []
        dir_name = os.path.basename(sub_dir)
        file_glob = os.path.join(TRAINING_DATA_DIR, dir_name, "*.jpg")
        file_list.extend(glob.glob(file_glob))
        if not file_list: continue

        label = int(dir_name)
        training_images = []
        validation_images = []
        for file_name in file_list:
            base_name = os.path.basename(file_name)

            #TODO:根据随机数进行划分训练集和验证集，不能完全精确按照配置的比例划分
            chance = np.random.randint(100)
            if chance < VALIDATION_PERCENTAGE:
                validation_images.append(base_name)
            else:
                training_images.append(base_name)
        result[label] = {
            "dir": dir_name,
            "training": training_images,
            "validation": validation_images
        }
    #测试集
    sub_dirs = [x[0] for x in os.walk(TEST_DATA_DIR)]
    for sub_dir in sub_dirs[1:]:
        file_list = []
        dir_name = os.path.basename(sub_dir)
        file_glob = os.path.join(TEST_DATA_DIR, dir_name, "*.jpg")
        file_list.extend(glob.glob(file_glob))
        if not file_list: continue

        label = int(dir_name)
        test_images = [os.path.basename(x) for x in file_list]
        result[label]["testing"] = test_images
    #处理空测试集
    for key in result.keys():
        if "testing" not in result[key]:
            result[key]["testing"] = {}
    if isTestSelfTrain:
        print("over creat_list")
        print(result)

    return result

image_cache = {}
def read_image_with_cache(dir_name, file_name, category):
    '''
    获取一张图片的数据，内部使用了缓存机制
    :param dir_name:图片所保存目录名，不可传入完整目录，只需要最后一个目录
    eg: /path/to/tmp (错误)
            tmp (正确)
    :param file_name:图片文件名，不可包含目录，只需要文件名
    :param category:待求图片所属集合，取值(training | validation | testing)
    :return: 图片数据
    '''
    key = os.path.join(category, dir_name, file_name)
    if key in image_cache:
        return image_cache[key]
    else:
        if "testing" == category:
            file_with_path = os.path.join(TEST_DATA_DIR, dir_name, file_name)
        else:
            file_with_path = os.path.join(TRAINING_DATA_DIR, dir_name, file_name)
        image = Image.open(file_with_path)
        image_array = np.array(image, dtype=np.float32) / 1000.
        image_cache[key] = image_array
        return image_array

def read_image(path):
    '''
    获取一张图片的数据，不使用缓存机制
    :param path:  图片文件路径
    :return: 图片数据
    '''
    image = Image.open(path)
    image_array = np.array(image, dtype=np.float32) / 1000.
    return image_array

def read_image_resize(path):
    '''
    获取一张图片的数据，不使用缓存机制
    :param path:  图片文件路径
    :return: 图片数据
    '''
    image = Image.open(path)
    image = image.resize((leNet5Inference.IMAGE_SIZE, leNet5Inference.IMAGE_SIZE))
    image_array = np.array(image, dtype=np.float32) / 1000.
    return image_array

image_lists = create_image_lists()
def get_train_batch(num):
    '''
    获取一个训练集合
    :param num: 数量
    :return: 包含num个元素的训练集合
    '''
    batches = []
    ground_truths = []

    n_classes = len(image_lists)
    for _ in range(num):
        label_index = np.random.randint(n_classes)
        image_index = np.random.randint(len(image_lists[label_index]["training"]))
        batch = read_image_with_cache(
            image_lists[label_index]["dir"],
            image_lists[label_index]["training"][image_index],
            "training"
        )
        ground_truth = np.zeros(n_classes, dtype=np.float32)
        ground_truth[label_index] = 1.0
        batches.append(batch)
        ground_truths.append(ground_truth)
    return batches, ground_truths


def get_validation_set():
    '''
    获取验证集合
    :return: 验证集合
    '''
    batches = []
    ground_truths = []
    n_classes = len(image_lists)
    for label_index, images in image_lists.items():
        for image in images["validation"]:
            file_with_path = os.path.join(TRAINING_DATA_DIR, images["dir"], image)
            batch = read_image(file_with_path)
            ground_truth = np.zeros(n_classes, dtype=np.float32)
            ground_truth[label_index] = 1.0
            batches.append(batch)
            ground_truths.append(ground_truth)
    return batches, ground_truths

def get_test_set(num):
    '''
    获取测试集合
    :return: 测试集合
    '''
    '''
    batches = []
    ground_truths = []
    n_classes = len(image_lists)
    for label_index, images in image_lists.items():
        for image in images["testing"]:
            file_with_path = os.path.join(TEST_DATA_DIR, images["dir"], image)
            batch = read_image(file_with_path)
            ground_truth = np.zeros(n_classes, dtype=np.float32)
            ground_truth[label_index] = 1.0
            batches.append(batch)
            ground_truths.append(ground_truth)
    return batches, ground_truths
    '''
    batches = []
    ground_truths = []

    n_classes = len(image_lists)
    for _ in range(num):
        label_index = np.random.randint(n_classes)
        image_index = np.random.randint(len(image_lists[label_index]["testing"]))
        batch = read_image_with_cache(
            image_lists[label_index]["dir"],
            image_lists[label_index]["testing"][image_index],
            "testing"
        )
        ground_truth = np.zeros(n_classes, dtype=np.float32)
        ground_truth[label_index] = 1.0
        batches.append(batch)
        ground_truths.append(ground_truth)
    return batches, ground_truths

