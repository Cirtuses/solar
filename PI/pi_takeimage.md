# this is the description of pi_takeimage.py

## pi_takeimage.py
    use PI to take images of the sky.

## start take
    在拍照之前一定要设置好树莓派的摄像头调用权限

    you can choose to take HR images or LR images through setting the argument of LR_or_HR
    HR分辨率为1600*1200 LR分辨率为640*480
    选择拍摄HR，拍照的时间间隔为10s 反之LR的拍照时间间隔为5s
    exposures设置成[100, 450, 700]

    save_path : 存放 images 的path
    
    可以在main函数里设置拍照的开始和结束时间