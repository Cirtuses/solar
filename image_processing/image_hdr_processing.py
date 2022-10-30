# encoding:utf8
import threading

import cv2
import numpy as np
import os
from natsort import ns, natsorted

index = 1
resolution = ['LR', 'HR']
date = ['20220112']
#path=r'C:\Users\lucky_wang\OneDrive\二年级\太阳能\csv\v1\sub1'
root_path = "/media/nucleus/solar/TongJi5F-LRHR/" + date[0] + '/'
save_path = "/media/nucleus/solar/TongJi5F-LRHR/" + date[0] + '/'


def robertson(img_fn, imgs_path, save_path, count):
    # 第一阶段将所有图像加载到列表中，此外，需要常规HDR的曝光时间
    # 需要注意数据类型：图像应为1通道或3通道8位（np.uint8），曝光时间需要为np.float32，以秒为单位
    # img_fn = ['1tl.jpeg', '2tr.jpeg', '3bl.jpeg', '4br.jpeg']
    img_list = [cv2.imread(imgs_path + fn) for fn in img_fn]
    expo = [100, 450, 700]
    exposure_times = np.array([1 / i for i in expo], dtype=np.float32)
    # exposure_times = np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32)

    # 将曝光序列合并成一个HDR图像，显示了在OpenCV中求高动态范围成像的两种算法：Debvec和Robertson，
    # HDR图像的类型为float32，而不是uint8,因为它包含所有曝光图像的完整动态范围
    merge_robertson = cv2.createMergeRobertson()
    hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())

    # 将32位浮点HDR数据映射到范围[0..1]。实际上，在某些情况下，值可能大于1或低于0，所以注意我们以后不得不剪切数据，以避免溢出。
    tonemap2 = cv2.createTonemapDrago(gamma=1.3)
    tonemap2.process(hdr_robertson.copy())

    merge_mertens = cv2.createMergeMertens()
    res_mertens = merge_mertens.process(img_list)

    # Convert datatype to 8-bit and save
    # 为了保存或显示结果，我们需要将数据转换为[0..255]范围内的8位整数。
    res_mertens_8bit = np.clip(res_mertens * 255, 0, 255).astype('uint8')

    cv2.imwrite(save_path + "%d.jpg" % count, res_mertens_8bit)
    pass


"""
Read the images in the files and do the HDR
input image format: id0_iso100_expo450_(2020-12-25 09-00-00).jpg
output image format: <n>.jpg
"""
if __name__ == '__main__':
    # combine every 3 images
    for day in date:
        total = 0
        dst_path = save_path + resolution[index] + '-HDR/'
        os.mkdir(dst_path)
        img_path = root_path + resolution[index] + '/'
        imgs = os.listdir(img_path)
        #  id0_iso100_expo450_(2020-12-21 09-00-00).jpg
        # for img in imgs:
        #     if img[-19:-17] == "12":
        #         imgs.remove(img)
        imgs = natsorted(imgs)
        img_num = len(imgs)
        #print(imgs)
        for j in range(0, img_num, 3):
            thread = threading.Thread(target=robertson, args=(imgs[j:min(j + 3, img_num)], img_path, dst_path, total))
            thread.run()
            total += 1
        print("%s ,count is %d" % (day, total))
