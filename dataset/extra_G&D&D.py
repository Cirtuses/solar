import shutil
import pandas as pd
import os
import csv
import sys
from natsort import ns, natsorted

""" 
    make the training data

    Args:
        LR_or_HR: type
        GHI: 'total_Avg' 
        DHI: 'diffuse_Avg'
        TIME: 'TMSTAMP'
        DNI: 'DNI'
        interval_time: interval
        delay_time: delay
        dst_path:  destination data
        data_path:  source data
        csv_file_path:  message csv
        csv_filename:  csv file name
    Returns: 
"""

LR_or_HR = 'LR'
GHI = 'total_Avg'
DHI = 'diffuse_Avg'
TIME = 'TMSTAMP'
DNI = 'DNI'
# interval_time = 60
# delay_time = 10 
interval_time = int(sys.argv[1]) # interval
delay_time = int(sys.argv[2]) # horizon 

dataset_path = r'F:\dataset'

dst_path = os.path.join(dataset_path, str(delay_time // 60) + 'min-' + str(interval_time) + 's', DNI,
                        LR_or_HR)
# train_data_path = '/media/nucleus/solar/TongJi5F-LRHR/train_summer'
# test_data_path = '/media/nucleus/solar/TongJi5F-LRHR/test_summer'
train_data_path = r'F:\TongJi5F-LRHR\train_summer'
test_data_path = r'F:\TongJi5F-LRHR\test_summer'

# csv_file_path = '/media/nucleus/solar/data_set' + '/' + str(delay_time // 60) + 'min-' + str(
#     interval_time) + 's' + "/" + DNI + "/"  #数据集命名 horzion + interval

csv_file_path = os.path.join(dataset_path, str(delay_time // 60) + 'min-' + str(interval_time) + 's', DNI)

csv_filename =  os.path.join(csv_file_path , "data_" + str(delay_time // 60) + 'min_' + LR_or_HR + ".csv")

# fixed parameters0

interval = 5 if LR_or_HR == 'LR' else 10
# step = 60 // interval
step = interval_time // interval
file_step = delay_time // interval
# LR: 6121; HR: 3061
total = 6121 if LR_or_HR == 'LR' else 3061
range_per_day = total - file_step
num_per_day = range_per_day // step  # global index
csv_offset = 1 if LR_or_HR == 'LR' else 1
offset = delay_time / interval


def dateparse(timestamp):
    return pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')


def read_csv(path):
    os.chdir(path)
    filename_list = os.listdir(path)
    for file in filename_list:
        if file == LR_or_HR + '_information_.csv':
            data = pd.read_csv(file, encoding='gbk', date_parser=dateparse, header=None) 

            data.columns = ['photo_index', TIME, GHI, DHI, DNI]
            return data


def generate_data(path, data, index, flag):
    filename_list = os.listdir(path)
    filename_list = natsorted(filename_list)
    # print(filename_list)
    cnt = 0
    total = len(filename_list) // 3
    print(path)
    print(total)
    # return total
    range_per_day = total - file_step
    exposure_flag = 0
    for i in range(0, range_per_day, step):
        used_name = os.path.join(path, filename_list[3*i + 1])
        #used_name = os.path.join(path, str(i) + '.jpg')
        data_index = (i + offset) * csv_offset
        # if int(data[GHI][data_index]) < 200:
        #     exposure_flag = 0
        # else:
        #     exposure_flag = 1
        new_name = os.path.join(dst_path, flag,
                                str(cnt + index) + "-" + str(data[TIME][data_index]).replace(':', '-') + "-" + str(
                                    int(data[GHI][data_index])) + "-" + str(int(data[DHI][data_index])) + "-" + str(
                                    int(data[DNI][data_index])) + "-" + ".jpg")
        print(used_name, '==>', new_name)
        with open(csv_filename, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            try:
                row = [cnt + index, str(data[TIME][data_index]).replace(':', '-'), str(int(data[GHI][data_index])),
                       str(int(data[DHI][data_index])), str(int(data[DNI][data_index]))]
                # print(row)
                writer.writerow(row)
            except:
                print('2')
            csvfile.close()
        cnt += 1
        shutil.copyfile(used_name, new_name)
    return cnt


def excute(path, index, flag):
    data = read_csv(path)
    # path1 = os.path.join(path, LR_or_HR + '-HDR/') #从HR—HDR读数据
    path2 = os.path.join(path, LR_or_HR) # 直接送LR 读数据
    return generate_data(path2, data, index, flag)


def main(): 
    if not os.path.exists(dst_path):
        train_path = os.path.join(dst_path, "train")
        test_path = os.path.join(dst_path, "test")
        os.makedirs(train_path)
        os.makedirs(test_path)
    if not os.path.isfile(csv_filename):
        print(csv_filename)
        # os.mknod(csv_filename)
        open(csv_filename, 'wb')
    file_list_1 = os.listdir(train_data_path)
    file_list_2 = os.listdir(test_data_path)
    file_list_1.sort()
    file_list_2.sort()
    index = 0
    for file in file_list_1:
        cumulative_quantity = excute(os.path.join(train_data_path, file), index, "train")
        index += cumulative_quantity
    for file in file_list_2:
        cumulative_quantity = excute(os.path.join(test_data_path, file), index, "test")
        index += cumulative_quantity


if __name__ == "__main__":
    main()
