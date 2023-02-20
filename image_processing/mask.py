import numpy as np
import os
import cv2

dir_path = r"D:\solar\17\20210530"
source_picture = os.path.join(dir_path, "0.jpg")
destination_picture = os.path.join(dir_path, "0_after_mask.jpg")

def make_mask(src_picture, th_num):
    image = cv2.imread(src_picture)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (T, mask_image) = cv2.threshold(gray_image, th_num, 255, cv2.THRESH_BINARY)
    cv2.imshow("mask", mask_image)
    cv2.waitKey(0)
    # cv2.imwrite("generated_template.jpg", mask_image)
    return mask_image

def mask_process(template, src_picture):
    src_picture = cv2.imread(src_picture)
    masked = cv2.bitwise_and(src_picture, src_picture, mask=template)
    cv2.imshow("ans", masked)
    cv2.imwrite(destination_picture, masked)
    cv2.waitKey(0)
    
def mask_dataset(template, img): #用于处理数据集
    cv2_img = cv2.imread(img)
    masked = cv2.bitwise_and(cv2_img, cv2_img, mask=template)
    return Image.fromarray(cv2.cvtColor(masked, cv2.COLOR_BGR2RGB))

def main():
    template_picture = "LR.jpg"
    threshold_number = 140
    template = make_mask(template_picture, threshold_number)
    # source_picture = "0.jpg"
    mask_process(template, source_picture)
    
    
if __name__ == '__main__':
    main()
