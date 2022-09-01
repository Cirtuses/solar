import os
import numpy as np
import torch
import time
from torchvision import transforms
from PIL import Image
from config import parsers
import gc
import cv2

'''
Add a mask to an image
'''
def mask(img, mask_image):
    cv2_img = cv2.imread(img)
    masked = cv2.bitwise_and(cv2_img, cv2_img, mask=mask_image)
    return Image.fromarray(cv2.cvtColor(masked, cv2.COLOR_BGR2RGB))


if __name__ == '__main__':
    opt = parsers()
    train_path = opt.cal_mean_std_path
    add_mask = opt.mask
    image_mask = cv2.imread("LR.jpg")
    gray_image = cv2.cvtColor(image_mask, cv2.COLOR_BGR2GRAY)
    (T, mask_image) = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)

    imgs = [os.path.join(train_path, i) for i in os.listdir(train_path)]
    # Crop the center of the picture to 480 * 480
    trans = transforms.Compose([
        transforms.CenterCrop(480),
        transforms.ToTensor()
    ])
    img_num = float(len(imgs))
    mean_tmp = np.array([0.0, 0.0, 0.0])
    std_tmp = np.array([0.0, 0.0, 0.0])
    cal_num = 0.0
    data = []

    # Take 2000 pictures as the unit, calculate mean and std respectively,
    # and finally take the average value
    for i in range(len(imgs)):
        if add_mask == 0:
            tmp = trans(Image.open(imgs[i])).numpy()
        else:
            tmp = trans(mask(imgs[i], mask_image)).numpy()
        mean_tmp[0] = mean_tmp[0] + np.mean(tmp[0, :, :])
        mean_tmp[1] = mean_tmp[1] + np.mean(tmp[1, :, :])
        mean_tmp[2] = mean_tmp[2] + np.mean(tmp[2, :, :])
        if ((i + 1) % 2000 == 0) or ((i + 1) == len(imgs)):
            cal_num = cal_num + 1.0
            data.append(tmp)
            data = np.array(data)
            std_tmp[0] = std_tmp[0] + np.std(data[:, 0, :, :])
            std_tmp[1] = std_tmp[1] + np.std(data[:, 1, :, :])
            std_tmp[2] = std_tmp[2] + np.std(data[:, 2, :, :])
            del data
            gc.collect()
            data = []
        else:
            data.append(tmp)

    mean_tmp = mean_tmp / img_num
    std_tmp = std_tmp / cal_num
    # Output calculation results of mean and standard deviation
    print('mean:')
    print(mean_tmp)
    print('std:')
    print(std_tmp)