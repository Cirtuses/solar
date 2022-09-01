import numpy as np
import os
import cv2
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image


class MyDataSet(Dataset):
    """
    Data processing and loading of training sets and validation sets

        img_path: data set path
        train: true is the training set, false is the verification set
        target_label: labels requiring training and prediction (GHI, DHI, DNI)
        add_mask: whether to add a mask to the picture (0 is not added, 1 is added)
    """

    def __init__(self, img_path, train=True, transform=None, target_label='ghi', add_mask=0):
        self.label = target_label
        self.add_mask = add_mask
        self.file_path = img_path
        self.imgs = [os.path.join(self.file_path, i) for i in os.listdir(self.file_path)]
        self.img_num = len(self.imgs)

        self.image_mask = cv2.imread("LR.jpg")
        self.gray_image = cv2.cvtColor(self.image_mask, cv2.COLOR_BGR2GRAY)
        (T, self.mask_image) = cv2.threshold(self.gray_image, 140, 255, cv2.THRESH_BINARY)

        # Standardize data sets
        self.normalize = transforms.Normalize(
            mean=[0.4922, 0.5424, 0.5440],
            std=[0.2952, 0.3117, 0.3254]
        )
        if train:
            self.trans = transforms.Compose([
                transforms.CenterCrop(480),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                self.normalize
            ])
        else:
            self.trans = transforms.Compose([
                transforms.CenterCrop(480),
                transforms.ToTensor(),
                self.normalize
            ])

        self.date_list = []
        for i in range(self.img_num):
            date = ""
            date_arr = (self.imgs[i].split('/')[-1].split('-')[1:6])
            n = len(date_arr)
            for j in range(n):
                date += date_arr[j]
                if (j == 0 or j == 1):
                    date += "-"
                if (j == 2 or j == 3):
                    date += ":"
                self.date_list.append(date)


    def mask(self, img, mask_image):
        # Function to add mask
        cv2_img = cv2.imread(img)
        masked = cv2.bitwise_and(cv2_img, cv2_img, mask=mask_image)
        return Image.fromarray(cv2.cvtColor(masked, cv2.COLOR_BGR2RGB))


    def __getitem__(self, index):
        if self.add_mask == 0:
            data_tmp = self.trans(Image.open(self.imgs[index]))
        else:
            data_tmp = self.trans(self.mask(self.imgs[index], self.mask_image))

        target_tmp = None
        # Process tags that need to be predicted
        if self.label == 'ghi':
            target_tmp = float(self.imgs[index].split('/')[-1].split('-')[6]) / 1000.0
            target_tmp = torch.tensor(target_tmp)
        elif self.label == 'dhi':
            target_tmp = float(self.imgs[index].split('/')[-1].split('-')[7]) / 600.0
            target_tmp = torch.tensor(target_tmp)
        elif self.label == 'dni':
            target_tmp = float(self.imgs[index].split('/')[-1].split('-')[8]) / 800.0
            target_tmp = torch.tensor(target_tmp)

        date_tmp = self.date_list[index]

        return data_tmp, target_tmp, date_tmp

    def __len__(self):
        return self.img_num


class MyDataSetTest(Dataset):
    """
    Data processing and loading of test set

        img_path: data set path
        target_label: labels requiring prediction (GHI, DHI, DNI)
        add_mask: whether to add a mask to the picture (0 is not added, 1 is added)
    """

    def __init__(self, img_path, transform=None, target_label='ghi', add_mask=0):
        self.label = target_label
        self.file_path = img_path
        self.add_mask = add_mask
        self.imgs = [os.path.join(self.file_path, i) for i in os.listdir(self.file_path)]
        #self.imgs = sorted(self.imgs, key=lambda x: int(x.split('/')[-1].split('-')[0].split('\\')[1]))
        self.imgs = sorted(self.imgs, key=lambda x: int(x.split('/')[-1].split('-')[0]))
        self.img_num = len(self.imgs)

        self.image_mask = cv2.imread("LR.jpg")
        self.gray_image = cv2.cvtColor(self.image_mask, cv2.COLOR_BGR2GRAY)
        (T, self.mask_image) = cv2.threshold(self.gray_image, 140, 255, cv2.THRESH_BINARY)


        # Standardize data sets
        self.normalize = transforms.Normalize(
            mean=[0.4922, 0.5424, 0.5440],
            std=[0.2952, 0.3117, 0.3254]
        )
        self.trans = transforms.Compose([
            transforms.CenterCrop(480),
            transforms.ToTensor(),
            self.normalize
        ])


        self.date_list = []
        for i in range(self.img_num):
            date = ""
            date_arr = (self.imgs[i].split('/')[-1].split('-')[1:6])
            n = len(date_arr)
            for j in range(n):
                date += date_arr[j]
                if (j == 0 or j == 1):
                    date += "-"
                if (j == 2 or j == 3):
                    date += ":"
            self.date_list.append(date)


    def mask(self, img, mask_image):
        # Function to add mask
        cv2_img = cv2.imread(img)
        masked = cv2.bitwise_and(cv2_img, cv2_img, mask=mask_image)
        return Image.fromarray(cv2.cvtColor(masked, cv2.COLOR_BGR2RGB))


    def __getitem__(self, index):
        if self.add_mask == 0:
            data_tmp = self.trans(Image.open(self.imgs[index]))
        else:
            data_tmp = self.trans(self.mask(self.imgs[index], self.mask_image))
        target_tmp = None
        # Process tags that need to be predicted
        if self.label == 'ghi':
            target_tmp = float(self.imgs[index].split('/')[-1].split('-')[6]) / 1000.0
            target_tmp = torch.tensor(target_tmp)
        elif self.label == 'dhi':
            target_tmp = float(self.imgs[index].split('/')[-1].split('-')[7]) / 600.0
            target_tmp = torch.tensor(target_tmp)
        elif self.label == 'dni':
            target_tmp = float(self.imgs[index].split('/')[-1].split('-')[8]) / 800.0
            target_tmp = torch.tensor(target_tmp)

        date_tmp = self.date_list[index]

        return data_tmp, target_tmp, date_tmp

    def __len__(self):
        return self.img_num