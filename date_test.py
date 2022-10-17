import pandas as pd 
import numpy as np
import datetime


def convert_pressure(num):
    return float(num)*2


# def convert_grades(df):  # 量化数据库，传入Dataframe数据类型
#     return df.applymap(convert_to_number)

def dateparse_year(timestamp):
    #07/21/21 下午06时34分00秒
    timestamp = timestamp.replace('上午', 'AM')
    timestamp = timestamp.replace('下午', 'PM')
    time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    return time.year

def dateparse_month(timestamp):
    #07/21/21 下午06时34分00秒
    timestamp = timestamp.replace('上午', 'AM')
    timestamp = timestamp.replace('下午', 'PM')
    time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    return time.month

def dateparse_day(timestamp):
    #07/21/21 下午06时34分00秒
    timestamp = timestamp.replace('上午', 'AM')
    timestamp = timestamp.replace('下午', 'PM')
    time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    return time.day

def dateparse_hour(timestamp):
    #07/21/21 下午06时34分00秒
    timestamp = timestamp.replace('上午', 'AM')
    timestamp = timestamp.replace('下午', 'PM')
    time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    return time.hour

def weather_process(file):
    data = pd.read_csv(file, header=1, usecols=[1,2,3,4,5,6,8]) # 从csv文件中读出对应的列
    print(data)
    data.columns = ['TIME', 'Atmos Pressure', 'Dry Bulb Temperature', 'Relative Humidity', 'Wind Direction', 'Wind Speed', 'Dew Point Temperature']

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

   
    #data['TIME'] = data['TIME'].astype(np.int)
    print(result)
    result.to_csv('data2.csv', header=0,index=0, sep=' ')

def csv_merge(file1, file2):
    return 
    




def main():
    file = '21-6-30 To 21-7-21.csv'
    weather_process(file)

if __name__ == '__main__':
    main()
