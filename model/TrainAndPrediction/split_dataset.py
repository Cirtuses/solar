import numpy as np
import os
from shutil import copy
import random
from config import parsers

'''
The original training set is divided into training set and verification set by 8:2
    source_path: the path of the original data set
'''
def split_file_list(source_path):
    imgs = [os.path.join(source_path, i) for i in os.listdir(source_path)]
    random.shuffle(imgs)
    img_num = len(imgs)
    return imgs[:int(img_num * 0.8)], imgs[int(img_num * 0.8):]


if __name__ == '__main__':
    opt = parsers()
    # The dataset is divided into training set, verification set and test set

    # The training set and the verification set are divided from the original training set,
    # and the test set is the original test set。
    file_path = opt.source_train_path
    test_path = opt.source_test_path
    train_path = opt.target_train_path
    val_path = opt.target_val_path
    test_target_path = opt.target_test_path
    train_files, val_files = split_file_list(file_path)
    test_files = [os.path.join(test_path, i) for i in os.listdir(test_path)]
    for i in range(len(train_files)):
        copy(train_files[i], train_path)
    for i in range(len(val_files)):
        copy(val_files[i], val_path)
    for i in range(len(test_files)):
        copy(test_files[i], test_target_path)

    print('Data set partition completed!')
