from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys



def dateparse(timestamp):
    #   07/21/21 下午06时34分00
    time = pd.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return time

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

    plt.plot(time, data["Measurement"], "-" , label="Measurement")
    plt.plot(time, data["Nowcasting"], "-", label="Nowcasting")
    #plt.plot(time, data["base_ghi"], "-", label="Generate")
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

    plt.savefig("../figures/{}.png".format(irradiance.lower() + "_" + interval.__str__() + "s_" + '2021-05-09'))
    plt.show()


def one_day(f, irradiance: str, interval: int, start, stop, flag = True):
    # if irradiance == "DNI":
    #     time = f.iloc[start:stop, 1]
    #     time.index = range(0, stop-start)
    #
    #     observation = f.iloc[start:stop, 2]
    #     observation.index = range(0, stop-start)
    #     nowcasting = f.iloc[start:stop, 3]
    #     nowcasting.index = range(0, stop-start)
    # else:
    time = f.iloc[start:stop, 0]
    time.index = range(0, stop-start)



    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, len(time) - 1)
        return time.at[thisind][11:-3]  # 2021-05-27 09:00:00


    #fig = plt.figure(figsize=(20,8), dpi = 500) #定义画布的大小

#划分子图
    
    #fig,axes = plt.subplots(2, 4, figsize=(20,8),sharey = True,constrained_layout=True, dpi = 600) #定义子区间的个数，注意第一个fig后面是逗号
    fig,axes = plt.subplots(2, 4, figsize=(20, 6),constrained_layout=True, dpi = 300) #定义子区间的个数，注意第一个fig后面是逗号

    ax = []
    for i in range(2):
        for j in range(4):
            ax.append(axes[i, j])

    for i in range(8):
        
        observation = f.iloc[start:stop, 1]
        observation.index = range(0, stop-start)
        nowcasting = f.iloc[start:stop, 2]
        nowcasting.index = range(0, stop-start)

        time = f.iloc[start:stop, 0]
        time.index = range(0, stop-start)

        start += 103
        stop += 103

        #ax[i].plot(time, observation, "-", label="Measurement")
        #ax[i].plot(time, nowcasting, "-", label="Nowcasting")
        
        ax[i].plot(time, observation, "-", label="Measurement")
        ax[i].plot(time, nowcasting, "-", label="Nowcasting")
        
        ax[i].legend()
        #plt.xlabel("Date/Time (hh:mm)")
        #ax1.set_xlabel("Date/Time (hh:mm)")
        if(i == 0):
            ax[i].set_ylabel("%s [W/${m^2}$]" % irradiance)
        if(i == 4):
            ax[i].set_ylabel("%s [W/${m^2}$]" % irradiance)
        #plt.ylabel("%s [W/${m^2}$]" % irradiance)
        #plt.gcf().subplots_adjust(left=0.08, right=0.96, top=0.90, bottom=0.2)

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
            idxLocator = plt.IndexLocator(6, 0)
        elif interval == 300:
            idxLocator = plt.IndexLocator(1, 0)

        ax[i].xaxis.set_major_locator(idxLocator)
        ax[i].xaxis.set_major_formatter(format_date)
        textstr = ' '.join((
        r'Year: %s' % (time.at[0][:4],),
        r'Date: %s' % (time.at[0][5:10],)))
        ax[i].set_title(textstr)
        my_y_ticks = np.arange(0, 1600, 200)
        ax[i].set_yticks(my_y_ticks)
        for label in ax[i].get_xticklabels():
            label.set_rotation(90)
        #ax[i].set_yticklabels([0, 200, 400, 600, 800, 1200])
            #label.set_size(6)
            #label.set_horizontalalignment('right')
        ax[i].grid()
        #ax[i].margins(y=0)



    #plt.suptitle('ghi_5min-300s')

    plt.savefig("../figures/{}.tiff".format(irradiance.lower() + "_" + interval.__str__() + "s_" + time.at[0][:10]))
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
   
    #path = "/Users/cirtus/Library/CloudStorage/OneDrive-个人/automation/2022-01-30/"
    path = r"C:\Users\lucky_wang\OneDrive\automation\result"
    os.chdir(path)
    file = 'dni_result'
    head = ["TIME", "Measurement", "Nowcasting", "WeightForecst"]
    head = ["Time", "Measurement", "Nowcasting"]
    f = pd.read_csv(file, names=head)
    # f['TIME']= f['TIME'].map(dateparse)
    # f["month"] = f["TIME"].map(lambda x: x.month)
    # f["day"] = f["TIME"].map(lambda x: x.day)
    
    # criteria = (f["month"] == 5 ) & (f["day"] == 9)
    # #criteria = ((f["month"] == 5 ) & (f["day"] == 9)) | ((f["month"] == 5 ) & (f["day"] == 30)) | ((f["month"] == 6 ) & (f["day"] == 25)) | ((f["month"] == 7 ) & (f["day"] == 1))
    # #criteria = ((f["month"] == 4 ) & (f["day"] == 25)) | ((f["month"] == 5 ) & (f["day"] == 20))
    # f = f[criteria]
    #y = f['Measurement'].to_numpy()
    y_hat = f['Nowcasting'].to_numpy()
    y_hat = np.where(y_hat >= 0, y_hat, 0)
    f["Nowcasting"] = y_hat
    
    
 

    #total(data, "GHI", "ghi_5min-60s")
    one_day(f, "GHI", 60, 0, 91, True) #103 一组 #824

    # parse_days(f, "DNI", 300)




if __name__ == '__main__':
    main()
