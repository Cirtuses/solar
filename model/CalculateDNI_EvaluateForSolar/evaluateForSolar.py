import datetime

import pandas as pd
import numpy as np
import csv
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error
from soupsieve import select


def dateparse(timestamp):
    #   07/21/21 下午06时34分00
    # print(type(timestamp))
    if timestamp.find('-') >= 0:
        time = pd.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    else:
        time = pd.datetime.strptime(timestamp, '%Y/%m/%d %H:%M')
    return time


def nRMSE(y, y_hat):
    return np.sqrt(mean_squared_error(y, y_hat)) / np.mean(y)


def RMSE(y, y_hat):
    return np.sqrt(mean_squared_error(y, y_hat))


def nMAE(y, y_hat):
    return mean_absolute_error(y, y_hat) / np.mean(y)


def MAE(y, y_hat):
    return mean_absolute_error(y, y_hat)


def MBE(y, y_hat):
    return np.mean((y_hat - y))


def MAPE(y, y_hat):
    return np.mean(np.abs(y_hat - y) / y) * 100


def R(y, y_hat):
    mean_p = y_hat.mean()
    mean_g = y.mean()
    sigma_p = y_hat.std()
    sigma_g = y.std()
    correlation = ((y_hat - mean_p) * (y - mean_g)).mean(axis=0) / (sigma_p * sigma_g)

    return correlation


def indicators(y, y_hat):
    mae = MAE(y, y_hat)
    nmae = nMAE(y, y_hat)
    rmse = RMSE(y, y_hat)
    nrmse = nRMSE(y, y_hat)
    r = R(y, y_hat)
    mape = MAPE(y, y_hat)
    mbe = MBE(y, y_hat)
    return mae, nmae, rmse, nrmse, r, mape, mbe


def main():
    dir_path = r"D:\PythonWorks\solar_project\Result_8-12"
    os.chdir(dir_path)

    dirlist = os.listdir(dir_path)
    # print(dirlist)

    for dir in dirlist:
        file_path = os.path.join(dir_path, dir)
        filename_list = os.listdir(file_path)
        # os.chdir(file_path)
        print(file_path)

        select_file = []
        for file in filename_list:
            if file.find("ghi") >= 0 and file.find("result") >= 0:
                select_file.append(file)

        for file in filename_list:
            if file.find("dhi") >= 0 and file.find("result") >= 0:
                select_file.append(file)

        for file in filename_list:
            if file.find("dni") >= 0 and file.find("result") >= 0:
                select_file.append(file)

        # print(select_file)
        # exit()

        for file in select_file:
            if file.find("ghi") >= 0 or file.find("dhi") >= 0 or file.find("dni") >= 0:  #
                file_tag = dir + ' ' + file
                file = os.path.join(file_path, file)
                # if file.find("dni") >=0:
                # head = ["Time", "Measurement", "Nowcasting", "WeightForecst"]
                print(file)
                head = ["Time", "Measurement", "Nowcasting"]
                f = pd.read_csv(file, header=0)
                f.columns = head
                print(f)

                # idx = 0
                # for ind, date in enumerate(f["Time"]):
                #     if datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").month > 9:
                #         idx = ind
                #         break

                f['Time'] = f['Time'].map(dateparse)
                f["month"] = f["Time"].map(lambda x: x.month)
                f["day"] = f["Time"].map(lambda x: x.day)
                # print(f["month"].month)

                # criteria = (f["Time"].month< 8760) & (df.index%2 == 0)
                # criteria = ((f["month"] == 5 ) & (f["day"] == 30))
                # criteria = ((f["month"] == 5 ) & (f["day"] == 22)) | ((f["month"] == 6 ) & (f["day"] == 21))
                # criteria = ((f["month"] == 5 ) & (f["day"] == 9)) | ((f["month"] == 5 ) & (f["day"] == 30)) | ((f["month"] == 6 ) & (f["day"] == 25)) | ((f["month"] == 7 ) & (f["day"] == 1))
                # criteria = ((f["month"] == 4 ) & (f["day"] == 25)) | ((f["month"] == 5 ) & (f["day"] == 20))
                # f = f[criteria]
                y = f['Measurement'].to_numpy()
                # y_hat = f['WeightForecst'].to_numpy()
                y_hat = f['Nowcasting'].to_numpy()
                # p = f['Measurement'].shift(1).to_numpy()
                # p = f['Nowcasting'].shift(1).to_numpy()
                # y_hat = p

                # y = np.where(y, y, 1)
                # y_hat = np.where(y_hat, y_hat, 1)
                y_hat = np.where(y_hat >= 0, y_hat, 0)

                # nowcasting = nowcasting.where(nowcasting > 0, 0)

                mae, nmae, rmse, nrmse, r, mape, mbe = indicators(y[0:], y_hat[0:])
                print("MAE: {}\n"
                      "nMAE: {}\n"
                      "RMSE: {}\n"
                      "nRMSE: {}\n"
                      "R: {}\n"
                      "MAPE: {} %\n"
                      "MBE: {}".format(mae, nmae, rmse, nrmse, r, mape, mbe))

                mae = round(mae, 2)
                nmae = round(nmae, 2)
                rmse = round(rmse, 2)
                nrmse = round(nrmse, 2)
                r = round(r, 4)
                mape = round(mape, 2)
                mape = str(mape) + "%"
                mbe = round(mbe, 2)

                # file_name = "3_another_result.csv"
                file_name = "result.csv"
                file_name = os.path.join(dir_path, file_name)

                if os.path.isfile(file_name) == True:
                    with open(file_name, 'a+', encoding="utf-8", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([file_tag, mae, nmae, rmse, nrmse, r, mape, mbe])
                        csvfile.close()

                else:
                    field_order = ["file_name", "MAE", "nMAE", "RMSE", "nRMSE", "R", "MAPE", "MBE"]
                    with open(file_name, 'w', encoding="utf-8", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(field_order)
                        writer.writerow([file_tag, mae, nmae, rmse, nrmse, r, mape, mbe])
                        csvfile.close()


if __name__ == '__main__':
    main()
