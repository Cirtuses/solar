import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def total(f, irradiance: str, img_name):
    if irradiance == "DNI":
        tmp = pd.to_datetime(f.iloc[:, 1], format="%Y-%m-%d %H:%M:%S")
        time = f.iloc[:, 1]
        measurement = f.iloc[:, 2]
        nowcasting = f.iloc[:, 3]
    else:
        tmp = pd.to_datetime(f.iloc[:, 0], format="%Y-%m-%d %H:%M:%S")
        time = f.iloc[:, 0]
        measurement = f.iloc[:, 1]
        nowcasting = f.iloc[:, 2]

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

    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, len(time) - 1)
        return time.at[thisind][5:10]  # 2021-05-27 09:00:00

    fig, ax = plt.subplots(figsize=(10, 3), dpi=500)
    plt.plot(time, measurement, "-", label="Measurement")
    plt.plot(time, nowcasting, "-", label="Nowcasting")
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


def one_day(f, irradiance: str, interval: int, start, stop):
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

    observation = f.iloc[start:stop, 1]
    observation.index = range(0, stop-start)
    nowcasting = f.iloc[start:stop, 2]
    nowcasting.index = range(0, stop-start)

    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, len(time) - 1)
        return time.at[thisind][11:-3]  # 2021-05-27 09:00:00

    fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
    plt.plot(time, observation, "-", label="Measurement")
    plt.plot(time, nowcasting, "-", label="Nowcasting")
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
        idxLocator = plt.IndexLocator(9, 0)
    elif interval == 300:
        idxLocator = plt.IndexLocator(1, 0)

    ax.xaxis.set_major_locator(idxLocator)
    ax.xaxis.set_major_formatter(format_date)
    plt.xticks(rotation=90)

    textstr = ' '.join((
        r'Year: %s' % (time.at[0][:4],),
        r'Date: %s' % (time.at[0][5:10],)))
    plt.title(textstr)
    plt.legend()
    plt.grid()

    plt.savefig("./figures/{}.png".format(irradiance.lower() + "_" + interval.__str__() + "s_" + time.at[0][:10]))
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
    head = ["Time", "Measurement", "Nowcasting", "WeightForecst"]
    f = pd.read_csv(r"/Users/congtsang/Library/CloudStorage/OneDrive-Personal/Archive/数据展示csv/2022-03-20/dhi_5min-300s_predict_all.csv",
                    names=head)
    # total(f, "GHI", "ghi_5min-300s")
    one_day(f, "DHI", 300, 0, 102)

    # parse_days(f, "DNI", 300)


if __name__ == '__main__':
    main()
