from time import sleep
import time
from picamera import PiCamera
import datetime
import os

""" 
    pi take the images

    Args:
        LR_or_HR: type
        interval: interval time
        count: number of images
        save_path:  destination data
        exposures:  exposure
        log:  log of the images
    Returns: 
"""
Time = datetime.datetime.now()
Time = time.strftime('%Y%m%d')

save_path = "/home/pi/Desktop/"
camera = PiCamera()
count = 0
exposures = [100, 450, 700]
LR_or_HR = "LR"
resolutions = [(1600, 1200)] if LR_or_HR == "HR" else [(640, 480)]
interval = 10  # Unit: second
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

def main():
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


if __name__ == '__main__':
    main()

    