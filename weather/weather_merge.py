
import os
import sys
import pandas as pd 
import numpy as np
import datetime
sys.path.append("..") 

from model.CalculateDNI_EvaluateForSolar import csv_calculate_DNI
# from CalculateDNI_EvaluateForSolar import csv_calculate_DNI


file1_path = r"D:\solar\sim_file"
# 21-12-8 To 21-12-29 || 21-11-18 To 21-12-9
# file1_path = os.path.join(file1_path, '21-8-10 To 21-8-31.csv')
file1_path = os.path.join(file1_path, '21-12-8 To 21-12-29.csv')

# 天气文件的path 天气文件 warning:预处理的时候，所有包含的日期都要完整并且保留表头信息


# 含有ghi dhi原始信息的csv
# file2_path = r"D:/solar/solar/20211018/20211018.csv"
# file2_path = os.path.join(file2_path, '20211018' , '20211018.csv') 


#或者 含有ghi_result.csv 和dhi_result.csv的文件夹
file2_path = r"D:\solar\sim_file\winter_day\60I_60H"


def convert_pressure(num):
    return float(num)*2

def dateparse1(timestamp):
    return pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

def dateparse2(timestamp):
#   07/21/21 下午06时34分00秒
    if timestamp.find('午') >= 0:
        timestamp = timestamp.replace('上午', 'AM')
        timestamp = timestamp.replace('下午', 'PM')
        time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    else:
        time = pd.datetime.strptime(timestamp, '%m/%d/%y %I:%M:%S %p')
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

def dateparse_minute(timestamp):
    return timestamp.minute

def dateparse_second(timestamp):
    return timestamp.second

def weather_pre_process(file, solar_data): #将气象站数据转化为天气文件的数据
    data = pd.read_csv(file, header=1, usecols=[1,2,3,4,5,6,8]) # 从csv文件中读出对应的列
    data.columns = ['TIME', 'Atmos Pressure', 'Dry Bulb Temperature', 'Relative Humidity', 'Wind Direction', 'Wind Speed', 'Dew Point Temperature']
    data['TIME']= data['TIME'].map(dateparse2)
    solar_data['TIME']= solar_data['TIME'].map(dateparse1)
    print(data)
    print(solar_data)
    
    
    # solar_data['Year']= data['TIME'].map(dateparse_year)
    # solar_data['Month']= data['TIME'].map(dateparse_month)
    # solar_data['Day'] = data['TIME'].map(dateparse_day)
    # solar_data['Hour'] = data['TIME'].map(dateparse_hour)
    # solar_data['Minute'] = data['TIME'].map(dateparse_minute)
    # solar_data['Second'] = data['TIME'].map(dateparse_second)
    
    
    # # criteria = (df["Month"] == 7 ) & (df["Day"] == 1) & (df["Minute"] == 0) & (df["Second"] == 0)
    # criteria = (solar_data["Month"] == 8 ) & (solar_data["Day"] == 29)
    # print(solar_data[criteria])
    
    # data['TIME']=data['TIME'].astype(str)
    # solar_data['TIME']=solar_data['TIME'].astype(str)
    print(type(data['TIME']))
    print(type(solar_data['TIME']))
    # exit()
    
    # data = data.join(solar_data, on='TIME')

    data = pd.merge(data,solar_data,how='left', on='TIME')
    print('融合之后的data:')
    data.to_csv('data_1min_measure_merge.csv')
    # exit()
    print(data)
    return data

def weather_process(data):
    result = pd.DataFrame()

    result['Year']= data['TIME'].map(dateparse_year)
    result['Month']= data['TIME'].map(dateparse_month)
    result['Day'] = data['TIME'].map(dateparse_day)
    result['Hour'] = data['TIME'].map(dateparse_hour)
    result['Minute'] = data['TIME'].map(dateparse_minute)
    result['Second'] = data['TIME'].map(dateparse_second)
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

    # result['Global Horizontal Radiation'] = data['ghi_predict'].map(lambda x:x*3600)
    # result['Diffuse horizontal radiation'] = data['dhi_predict'].map(lambda x:x*3600)
    # result['Direct Normal Radiation'] = data['dni_predict'].map(lambda x:x*3600)
    
    
    result['Global Horizontal Radiation'] = data['ghi_predict']
    result['Diffuse horizontal radiation'] = data['dhi_predict']
    result['Direct Normal Radiation'] = data['dni_predict'].map(lambda x:x if x > 0 else 0)

   
    #data['TIME'] = data['TIME'].astype(np.int)
    print(result)
    len = result.shape[0] 
    print(len)
    df = result
    criteria = (df.index < 8760) & (df.index%2 == 0)
    # criteria = (df["Month"] == 7 ) & (df["Day"] == 1) & (df["Minute"] == 0) & (df["Second"] == 0)
    criteria = (df["Month"] == 12 ) & (df["Day"] == 11) & (df["Second"] == 0)
    print(df[criteria])
    #result.to_csv('data2.csv', header=0,index=0, sep=' ')
    # df[criteria].to_csv('20210904_60I_60H.csv', header=0,index=0, sep=' ')
    # 1207 1208 1211
    df[criteria].to_csv('20211211_60I_60H.csv', header=0,index=0, columns=['Year', 'Month','Day', 'Hour', 'Atmos Pressure',
    'Dry Bulb Temperature', 'Relative Humidity', 'Wind Direction', 'Wind Speed', 'Dew Point Temperature',
    'Global Horizontal Radiation', 'Diffuse horizontal radiation', 'Direct Normal Radiation'], sep=' ')
    return df[criteria]
    #SONG WENT

def csv_merge(file1_path, file2_path):
    solar_data = pd.DataFrame()
    
    #获取DNI
    #solar_data['TIME'], solar_data['ghi_predict'], solar_data['dhi_predict'], solar_data['dni_predict'] = csv_calculate_DNI.calculate_dni_from_onefile(file2_path, False)
    
    #如果是含有ghi_result.csv 和dhi_result.csv的文件夹
    solar_data['TIME'], solar_data['ghi_predict'], solar_data['dhi_predict'], solar_data['dni_predict'] = csv_calculate_DNI.calculate_dni_from_twofile(file2_path, measure_flag=True)
    
    print(solar_data)
    df = weather_pre_process(file1_path, solar_data)
    weather_process(df)


def main():

    print(file1_path, file2_path)
    csv_merge(file1_path, file2_path) #file1为气象站数据 file2为辐射数据

if __name__ == '__main__':
    main()
