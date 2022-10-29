# solar


## dataset

    extra_G&D&D.py
        for making sloar dateset
        根据需求生成对应的图像

## image_processing

    image_hdr_processing.py
        for generating hdr images
        当我们用树莓派拍好图片之后，运行这个文件就可以将同一时刻三张不同曝光度的图片合成生成一张

## model

    csv_calculate_DNI.py
        利用GHI DHI来生成DNI
        Calculate the DNI through GHI and DHI.
    
    evaluateForSolar.py
        计算数据指标
        Evaluate precising and visualize the results

## PI

    pi_takeimage.py
        PI collects sky image.
        树莓派利用鱼眼相机拍天空的图片

## PI

    auto.sh
        Startup script. When the PI is powered on, it will execute the pi_takeimage.py

    pi_upload.py
        PI uploads images and log file to sftp database.

## weather

    weather_merge.py
        Fusion of weather and radiation files in csv format.


