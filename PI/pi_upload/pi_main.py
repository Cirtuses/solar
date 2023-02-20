from pi_upload import *
from pi_takeimage import takeImagesWithTime
from picamera import PiCamera
import cv2
import numpy as np

# 预备工作
Time = datetime.datetime.now()
Time = time.strftime('%Y%m%d')

save_path = "/home/pi/Desktop/"
camera = PiCamera()
count = 0
exposures = [100, 450, 700]
LR_or_HR = "LR"
resolutions = [(1600, 1200)] if LR_or_HR == "HR" else [(640, 480)]
interval = 300  # Unit: second
log = os.path.join(save_path, Time, LR_or_HR + 'log.txt')


save_path = os.path.join(save_path, Time)
if os.path.exists(save_path)==False:
    os.mkdir(save_path)
    os.mkdir(os.path.join(save_path, LR_or_HR))
    print("create DIR path")

def takeImagesWithTime(iso_values, st_time, save_path):
    global count
    for exposure in exposures:
        # Set ISO to the desired value
        camera.iso = iso_values
        # Wait for the automatic gain control to settle
        sleep(1)
        # Now fix the values
        camera.saturation = 0
        camera.sharpness = 0
        camera.brightness = 50
        camera.contrast = 0
        camera.shutter_speed = exposure
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        
        img_time = st_time.strftime("(%Y-%m-%d %H-%M-%S)")
        for i, resolu in enumerate(resolutions):
            camera.resolution = resolu
            # Finally, take several photos with the fixed settings
            picture_name = 'id{}_iso{}_expo{}_{}.jpg'.format(count, iso_values, exposure, img_time)
            save_picture = os.path.join(save_path, LR_or_HR, picture_name)
            camera.capture(save_picture) # image 名称
    count += 1


def robertson(img_fn, imgs_path, save_path, count):
    # 第一阶段将所有图像加载到列表中，此外，需要常规HDR的曝光时间
    # 需要注意数据类型：图像应为1通道或3通道8位（np.uint8），曝光时间需要为np.float32，以秒为单位
    # img_fn = ['1tl.jpeg', '2tr.jpeg', '3bl.jpeg', '4br.jpeg']
    img_list = [cv2.imread(os.path.join(imgs_path, fn)) for fn in img_fn]
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

    cv2.imwrite(os.path.join(save_path , "%d.jpg" % count), res_mertens_8bit)
    pass


if __name__ == '__main__': 
    #to do 加入hdr处理
    iso = 100
    signal = False
    record = False
    print("hello! Begin getting data")
    
    Time = datetime.datetime.now()
    Time = time.strftime('%Y%m%d')
    
    f = open(log, 'a+')  # logs
    while True:
        time_now = datetime.datetime.now()
        # print('\rTime: %s' %(time_now.strftime('%Y/%m/%d %H:%M:%S')), end='', flush=True)
        # if time_now.hour == 8 and time_now.minute == 59 and time_now.second == 58:
        if time_now.hour == 21 and time_now.minute == 43 and time_now.second == 58:
            record = True
            print('\nStart Record')
            break

    while record:
        time_now = datetime.datetime.now()
        # if time_now.hour == 22 and time_now.minute == 30:
        if time_now.hour == 22 and time_now.minute == 30:
            record = False
        if(time_now.second % interval == 0):
            signal = True

        if signal:
            #S = time.time()
            takeImagesWithTime(iso, time_now, save_path)
            
            
            
            
            
            f.write('%s\n' %(time_now.strftime('%Y/%m/%d %H:%M:%S')))
            signal = False
            #E = time.time()
            #print(E - S)
    f.flush()
    f.close()
    camera.close()
    print('Today is Done, have a rest.')
    
    # 首先拍照
    # 调用model获得GHI DHI
    # 利用这两个值计算得到DNI
    # upload
    
    #or
    # 拍照 然后upload

    main()
