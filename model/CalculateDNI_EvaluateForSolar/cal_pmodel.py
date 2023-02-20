import numpy as np
import pandas as pd


def dateparse(timestamp):
    #   07/21/21 下午06时34分00
    time = pd.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return time


if __name__ == "__main__":
    data_type = 'ghi'
    interval = 10
    herizion = 10
    read_path = r"D:\PythonWorks\solar_project\result_newData_10_10\10I_10H\ghi_result.csv"
    save_path = r"D:\PythonWorks\solar_project\result_newData_10_10\10I_10H"

    df_data = pd.read_csv(read_path)

    data_pre = int(herizion / interval)

    target_type = data_type + '_target'
    predict_type = data_type + '_predict'

    time_list = df_data['Time'].values
    target_list = df_data[target_type].values

    date_num_list = []
    date_flag = None
    for (i, date_tmp) in enumerate(time_list):
        date_day = date_tmp.split(' ')[0]
        if i == 0:
            date_num_list.append(0)
            date_flag = date_day
        else:
            if date_day != date_flag:
                date_num_list.append(i)
                date_flag = date_day
    date_num_list.append(len(time_list))

    newDateList = []
    newTargetList = []
    newPredictList = []

    for i in range(len(date_num_list)-1):
        newDateList = newDateList + list(time_list[date_num_list[i]+data_pre:date_num_list[i+1]])
        newTargetList = newTargetList + list(target_list[date_num_list[i]+data_pre:date_num_list[i+1]])
        newPredictList = newPredictList + list(target_list[date_num_list[i]:date_num_list[i+1]-data_pre])

    new_data = pd.DataFrame()
    new_data['Time'] = newDateList
    new_data[target_type] = newTargetList
    new_data[predict_type] = newPredictList

    new_data['Time'] = new_data['Time'].map(dateparse)

    save_path = save_path + '\\' + data_type + '_result.csv'
    new_data.to_csv(save_path, index=None)

