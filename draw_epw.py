import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys

from pyepw.epw import EPW


def dateparse(timestamp):
#   07/21/21 下午06时34分00秒
    timestamp = timestamp.replace('上午', 'AM')
    timestamp = timestamp.replace('下午', 'PM')
    time = pd.datetime.strptime(timestamp, '%m/%d/%y %p%I时%M分%S秒')
    # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time.strftime("%Y-%m-%d %H:%M:%S")

def weather_pre_process(file):
    data = pd.read_csv(file, header=1, usecols=[1,2,3,4,5,6,8]) # 从csv文件中读出对应的列
    data.columns = ['TIME', 'Atmos Pressure', 'Dry Bulb Temperature', 'Relative Humidity', 'Wind Direction', 'Wind Speed', 'Dew Point Temperature']
    data['TIME']= data['TIME'].map(dateparse)
    criteria = (data.index % 2 == 0)
    data = data[criteria]
    return data['TIME']

def total(data, irradiance: str, img_name):
    #total(f, "GHI", "ghi_5min-60s")
    if irradiance == "DNI":
        tmp = pd.to_datetime(data.iloc[:, 1], format="%Y-%m-%d %H:%M:%S")
        time = data.iloc[:, 1]
        measurement = data.iloc[:, 2]
        nowcasting = data.iloc[:, 3]
    elif irradiance == "DHI":
        tmp = pd.to_datetime(data.iloc[:, 0], format="%Y-%m-%d %H:%M:%S")
        time = data.iloc[:, 0]
        measurement = data.iloc[:, 1]
        nowcasting = data.iloc[:, 2]
    

    '''
    idx = 0
    for ind, date in enumerate(tmp):
        if date.month > 9:
            idx = ind
            break
    time = time[:idx]
    measurement = measurement[:idx]
    nowcasting = nowcasting[:idx]
    '''

    # measurement = measurement.where(measurement > 0, 1)
    # nowcasting = nowcasting.where(nowcasting < 1000, 0)
    time = data["TIME"]
    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, len(time) - 1)
        #print(time.at[thisind][5:10])
        return time.at[thisind][11:-3]  # 2021-05-27 09:00:00

    fig, ax = plt.subplots(figsize=(10, 3), dpi=500)
    plt.plot(time, data["measure_ghi"], "-" , label="Measurement")
    plt.plot(time, data["predict_ghi"], "-", label="Nowcasting")
    plt.plot(time, data["base_ghi"], "-", label="Generate")
    plt.xlabel("Date/Time (Y-m-d)")
    plt.ylabel("%s [W/${m^2}$]" % irradiance)
    plt.gcf().subplots_adjust(left=0.08, right=0.96, top=0.95, bottom=0.2)

    '''
    # 左上角文本
    textstr = ''.join("2021")
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.02, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    '''
    if img_name.find("10s") != -1:
        idxLocator = plt.IndexLocator(3000, 1500)
    elif img_name.find("60s") != -1:
        idxLocator = plt.IndexLocator(500, 250)
    elif img_name.find("300s") != -1:
        idxLocator = plt.IndexLocator(100, 50)
    elif img_name.find("600s") != -1:
        idxLocator = plt.IndexLocator(50, 25)

    ax.xaxis.set_major_locator(idxLocator)
    ax.xaxis.set_major_formatter(format_date)
    plt.legend()
    plt.grid()

    plt.savefig("./figures/{}.png".format(img_name))
    plt.show()


def one_day(data, irradiance: str, interval: int, start, stop):
    # if irradiance == "DNI":
    #     time = f.iloc[start:stop, 1]
    #     time.index = range(0, stop-start)
    #
    #     observation = f.iloc[start:stop, 2]
    #     observation.index = range(0, stop-start)
    #     nowcasting = f.iloc[start:stop, 3]
    #     nowcasting.index = range(0, stop-start)
    # else:
    #time = data.iloc[start:stop, 1]
    time = data["TIME"]
    #time.index = range(0, stop-start)
    print(time)

    observation = data.iloc[start:stop, 2]
    observation.index = range(0, stop-start)
    nowcasting = data.iloc[start:stop, 3]
    nowcasting.index = range(0, stop-start)

    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, len(time) - 1)
        return time.at[thisind][11:-3]  # 2021-05-27 09:00:00
        #return time.at[thisind].strftime('%H:%M:%S')  # 2021-05-27 09:00:00

    fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
    # plt.plot(time, observation, "-", label="Measurement")
    # plt.plot(time, nowcasting, "-", label="Nowcasting")
    plt.plot(time, data["measure_ghi"], "-" , label="Measurement")
    plt.plot(time, data["predict_ghi"], "-", label="Nowcasting")
    plt.plot(time, data["base_ghi"], "-", label="Generate")
    plt.xlabel("Date/Time (hh:mm)")
    plt.ylabel("%s [W/${m^2}$]" % irradiance)
    plt.gcf().subplots_adjust(left=0.08, right=0.96, top=0.90, bottom=0.2)
     
    '''
    # 左上角文本
    textstr = '\n'.join((
        r'Year: %s' % (time.at[0][:4],),
        r'Date: %s' % (time.at[0][5:10],)))
    props = dict(boxstyle='round', facecolor='white', alpha=0.2)
    ax.text(0.02, 0.95, textstr, transform=ax.transAxes, verticalalignment='top', bbox=props)
    '''
    if interval == 10:
        idxLocator = plt.IndexLocator(45, 0)
    elif interval == 60:
        idxLocator = plt.IndexLocator(30, 0)
    elif interval == 300:
        idxLocator = plt.IndexLocator(1, 0)

    ax.xaxis.set_major_locator(idxLocator)
    ax.xaxis.set_major_formatter(format_date)
    plt.xticks(rotation=90)
    
    # textstr = ' '.join((
        # r'Year: %s' % (time.at[0].strftime('%Y'),),
        # r'Date: %s' % (time.at[0].strftime('%m-%d'),)))
    textstr = ' '.join((
        r'Year: %s' % (time.at[0][:4],),
        r'Date: %s' % (time.at[0][5:10],)))
    plt.title(textstr)
    plt.legend()
    plt.grid()

    plt.savefig("./figures/{}.png".format(irradiance.lower() + "_" + interval.__str__() + "s_" + '2021-07-21'))
    plt.show()


def parse_days(f, irradiance: str, interval: int):
    if irradiance == "DNI":
        times = pd.to_datetime(f.iloc[:, 1], format="%Y-%m-%d %H:%M:%S")
    else:
        times = pd.to_datetime(f.iloc[:, 0], format="%Y-%m-%d %H:%M:%S")
    i = 0
    while i < len(times)-1:
        startT = times[i]
        start = i
        end = i
        for j in range(i + 1, len(times)):
            endT = times[j]
            if endT.day != startT.day:
                end = j
                i = j
                break
            if j == len(times)-1:
                end = j+1
                i = j
                break
        one_day(f, irradiance, interval, start, end)


def main():
   
    path = r'C:\Users\lucky_wang\OneDrive\automation'
    os.chdir(path)
    weather_file = os.path.join(path, '1min', '21-6-30 To 21-7-21.csv')
 
    predict_file = os.path.join(path, '1min', 'data_1min_predict.csv')
    measure_file = os.path.join(path, '1min', 'data_1min_predict.csv')


    epw_base_file = os.path.join(path, '1min', 'data_1min_base.epw')
    epw_predict_file = os.path.join(path, '1min', 'data_1min_predict.epw')
    epw_measure_file = os.path.join(path, '1min', 'data_1min_measure.epw')

    #predict_data = pd.read_csv(predict_file,header = None, usecols=[10], sep=' ') # 从csv文件中读出对应的列 usecols=[1,2,3,4,5,6,8]
    predict_data = pd.DataFrame(columns = ['ghi_predict'])
    base_data = pd.DataFrame(columns = ['ghi_predict'])
    measure_data = pd.DataFrame(columns = ['ghi_predict'])
    # predict_data.columns = ['ghi_predict']
    #measure
    # print(data.shape[0])
    

    predict_epw = EPW()
    predict_epw.read(epw_predict_file)

    # i = 0
    for wd in predict_epw.weatherdata:
        predict_data = predict_data.append([{'ghi_predict':wd.global_horizontal_radiation}], ignore_index=None)
    # print (wd.year, wd.month, wd.day, wd.hour, wd.minute, wd.atmospheric_station_pressure, wd.dry_bulb_temperature, wd.relative_humidity, wd.wind_direction, wd.wind_speed, wd.dew_point_temperature, wd.global_horizontal_radiation,
    #     wd.diffuse_horizontal_radiation, wd.direct_normal_radiation)
    #     print(wd.global_horizontal_radiation)
    #     print(data['ghi_predict'][i])
    #     wd.global_horizontal_radiation = data['ghi_predict'][i]
    #     print(wd.global_horizontal_radiation)    
    print(predict_data)
    predict_data = predict_data.reset_index()

    base_epw = EPW()
    base_epw.read(epw_base_file)
    for wd in base_epw.weatherdata:
        base_data = base_data.append([{'ghi_predict':wd.global_horizontal_radiation}], ignore_index=None)
    print(base_data)
    base_data = base_data.reset_index()

    measure_epw = EPW()
    measure_epw.read(epw_measure_file)
    for wd in measure_epw.weatherdata:
        measure_data = measure_data.append([{'ghi_predict':wd.global_horizontal_radiation}], ignore_index=None)
    print(measure_data)
    measure_data = measure_data.reset_index()
    
    
    data = pd.DataFrame()
    data['TIME'] = weather_pre_process(weather_file)
    data = data.reset_index()

    data['base_ghi'] = base_data['ghi_predict']
    data['measure_ghi'] = measure_data['ghi_predict']
    data['predict_ghi'] = predict_data['ghi_predict']

    #data.to_csv('pictrue.csv')
    #epw.save(r"new_file.epw")

    # head = ["Time", "Measurement", "Nowcasting", "WeightForecst"]
    # f = pd.read_csv(r'C:\Users\lucky_wang\OneDrive\automation\test_data\dhi_1min-60s_predict_all.csv',
    #                 names=head)
    

    #total(data, "GHI", "ghi_5min-60s")
    one_day(data, "GHI", 60, 0, 1440)

    # parse_days(f, "DNI", 300)




if __name__ == '__main__':
    main()
