import pandas as pd
import shutil
import os
import csv
import sys
sys.path.append('..')

from model.CalculateDNI_EvaluateForSolar.csv_calculate_DNI import calculate_dni_sourcefile #导入计算csv的文件

# parameters
LR_or_HR = 'LR'
GHI = 'total_Avg'
DHI = 'diffuse_Avg'
TIME = 'TMSTAMP'
DNI = 'DNI'
dir_path=r"F:\TongJi5F-LRHR\test_summer\20210829" 


csv_filename =  LR_or_HR + '_information_' + '.csv' # 新的包含有DNI的csv文件名

step = 1
total = 6121 if LR_or_HR == 'LR' else 3061 #天气图片数量
num_per_day = total # global index
csv_offset = 1 if LR_or_HR == 'LR' else 2 #步长
#csv_offset = 1 if LR_or_HR == 'LR' else 1


def dateparse(timestamp):
    return pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')


def generate_csv(dir_path):
    source_csv = os.path.join(dir_path, dir_path.split('\\')[-1] + '.csv') #例如 D:\solar\solar\20211018\20211018.csv
    save_name = os.path.join(dir_path, csv_filename) #例如 D:\solar\solar\20211018\HR_information_.csv
    print(save_name)
    calculate_dni_sourcefile(source_csv, True, save_name)
    

def main():
    '''
    global dir_path
    file_list = os.listdir(dir_path)
    for file in file_list:
        path = os.path.join(dir_path, file)
        data = generate_csv(path)
    '''

        
        
    generate_csv(dir_path)

if __name__ == "__main__":
    main()