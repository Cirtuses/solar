
import os
import sys
import pandas as pd 
import numpy as np
import datetime
sys.path.append("..") 
form model.CalculateDNI_EvaluateForSolar import csv_calculate_DNI


def convert_pressure(num):
    return float(num)*2

def dateparse(timestamp):
#   07/21/21 下午06时34分00秒
    timestamp = timestamp.replace('上午', 'AM')
    timestamp = timestamp.replace('下午', 'PM')
    time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    return time

# def dateparse_year(timestamp):

#     timestamp = timestamp.replace('上午', 'AM')
#     timestamp = timestamp.replace('下午', 'PM')
#     time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
#     return time.year
def dateparse_year(timestamp):
    #time = pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return timestamp.year

def dateparse_month(timestamp):
    #time = pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return timestamp.month

def dateparse_day(timestamp):
    #time = pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return timestamp.day

def dateparse_hour(timestamp):
    # #07/21/21 下午06时34分00秒
    # timestamp = timestamp.replace('上午', 'AM')
    # timestamp = timestamp.replace('下午', 'PM')
    # time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    #time = pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return timestamp.hour

def weather_pre_process(file, solar_data): #将气象站数据转化为天气文件的数据
    data = pd.read_csv(file, header=1, usecols=[1,2,3,4,5,6,8]) # 从csv文件中读出对应的列
    data.columns = ['TIME', 'Atmos Pressure', 'Dry Bulb Temperature', 'Relative Humidity', 'Wind Direction', 'Wind Speed', 'Dew Point Temperature']
    data['TIME']= data['TIME'].map(dateparse)
    data = pd.merge(data,solar_data,how='left',on='TIME')
    print('融合之后的data：')
    data.to_csv('data_1min_measure_merge.csv')
    print(data)
    return data

def weather_process(data):
    result = pd.DataFrame()

    result['Year']= data['TIME'].map(dateparse_year)
    result['Month']= data['TIME'].map(dateparse_month)
    result['Day'] = data['TIME'].map(dateparse_day)
    result['Hour'] = data['TIME'].map(dateparse_hour)
    #, 'Month', 'Day'
    print(result['Year'])
    
    data['Atmos Pressure'] = data['Atmos Pressure'].astype(np.float32)
    data['Dry Bulb Temperature'] = data['Dry Bulb Temperature'].astype(np.float32)
    data['Dew Point Temperature'] = data['Dew Point Temperature'].astype(np.float32)


    result['Atmos Pressure'] = data['Atmos Pressure'].map(lambda x:x*3386)

    result['Dry Bulb Temperature'] = data['Dry Bulb Temperature'].map(lambda x:(x-32)/1.8)

    result['Relative Humidity'] = data['Relative Humidity']
    result['Wind Direction'] = data['Wind Direction']
    result['Wind Speed'] = data['Wind Speed']
    
    result['Dew Point Temperature'] = data['Dew Point Temperature'].map(lambda x:(x-32)/1.8)
    # Global Horizontal Radiation, Diffuse horizontal radiation, Direct Normal Radiation,
    # solar_data['ghi_predict'], solar_data['dhi_predict'], solar_data['dni_predict']

    result['Global Horizontal Radiation'] = data['ghi_predict']
    result['Diffuse horizontal radiation'] = data['dhi_predict']
    result['Direct Normal Radiation'] = data['dni_predict']

   
    #data['TIME'] = data['TIME'].astype(np.int)
    print(result)
    len = result.shape[0] 
    print(len)
    df = result
    criteria = (df.index < 8760) & (df.index%2 == 0)
    print(df[criteria])
    #result.to_csv('data2.csv', header=0,index=0, sep=' ')
    df[criteria].to_csv('data_1min_measure.csv', header=0,index=0, sep=' ')
    return df[criteria]
    #SONG WENT

def csv_merge(file1_path, file2_path):
    solar_data = pd.DataFrame()
    
    
    # filename_list = os.listdir(file2_path)
    # print(filename_list)
    solar_data['TIME'], solar_data['ghi_predict'], solar_data['dhi_predict'], solar_data['dni_predict'] = csv_calculate_DNI.execute(file2_path)

    df = weather_pre_process(file1_path, solar_data)
    weather_process(df)




def main():
    path = r'C:\Users\lucky_wang\OneDrive\automation'
    file1_path = os.path.join(path, 'test_data', '21-6-30 To 21-7-21.csv') # 天气文件 warning:预处理的时候，所有包含的日期都要完整并且保留表头信息
    file2_path = os.path.join(path, 'test_data') # 包含有 ghi_file 和 dhi_file的文件位置
    print(file1_path, file2_path)
    csv_merge(file1_path, file2_path) #file1为气象站数据 file2为辐射数据

if __name__ == '__main__':
    main()
