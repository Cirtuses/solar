import datetime

import re
import pandas as pd
import numpy as np
import csv
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error
from soupsieve import select

# dir_path = r"D:\PythonWorks\solar_project\Result_8-12" ## win format
dir_path = "/Users/cirtus/Desktop/solar/test/solar/data/" ## 300-300


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

# SS-MAE SS-RMSE
def SS_MAE(y, y_hat, p):
    p_mae = MAE(y, p)
    f_mae = MAE(y, y_hat)
    print("SSMAE :{} {}".format(p_mae, f_mae))
    ss_mae = 1 - (f_mae / p_mae)
    return ss_mae * 100

def SS_RMSE(y, y_hat, p):
    p_rmse = RMSE(y, p)
    f_rmse = RMSE(y, y_hat)
    ss_rmse = 1 - (f_rmse / p_rmse)
    return ss_rmse * 100

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
                print("file \n")
                print(file)
                head = ["Time", "Measurement", "Nowcasting"]
                f = pd.read_csv(file, header=0)
                f.columns = head
                print("f \n")
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
                print(dir)
                number = re.findall("\d+",dir) 
                print(number)
                late = int(number[1]) // int(number[0])
                print(late)
                
                y = f['Measurement'].to_numpy()
                # y_hat = f['WeightForecst'].to_numpy()
                y_hat = f['Nowcasting'].to_numpy()
                p = f['Measurement'].shift(late).to_numpy()
                # p = f['Nowcasting'].shift(1).to_numpy()
                # y_hat = p

                # y = np.where(y, y, 1)
                # y_hat = np.where(y_hat, y_hat, 1)
                y_hat = np.where(y_hat >= 0, y_hat, 0)
                print("three")
                ## late
                

                # print(y[late:])
                # print(y_hat[late:])
                # print(p[late:])
                # exit()
                

                # nowcasting = nowcasting.where(nowcasting > 0, 0)

                mae, nmae, rmse, nrmse, r, mape, mbe = indicators(y[late:], y_hat[late:])
                # mae, nmae, rmse, nrmse, r, mape, mbe = indicators(y[late:], p[late:])
                # exit()
                
                ss_mae = SS_MAE(y[late:], y_hat[late:], p[late:])
                ss_rmse = SS_RMSE(y[late:], y_hat[late:], p[late:])
                print("MAE: {}\n"
                      "nMAE: {}\n"
                      "RMSE: {}\n"
                      "nRMSE: {}\n"
                      "R: {}\n"
                      "MAPE: {} %\n"
                      "MBE: {} \n"
                      "SS_MAE: {} %\n"
                      "SS_RMSE: {} %".format(mae, nmae, rmse, nrmse, r, mape, mbe, ss_mae, ss_rmse))

                mae = round(mae, 2)
                nmae = round(nmae, 2)
                rmse = round(rmse, 2)
                nrmse = round(nrmse, 2)
                r = round(r, 4)
                mape = round(mape, 2)
                mape = str(mape) + "%"
                mbe = round(mbe, 2)
                ss_mae = str(round(ss_mae, 2)) + "%"
                ss_rmse = str(round(ss_rmse, 2)) + "%"

                # file_name = "3_another_result.csv"
                file_name = "result.csv"
                file_name = os.path.join(dir_path, file_name)

                if os.path.isfile(file_name) == True:
                    with open(file_name, 'a+', encoding="utf-8", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([file_tag, mae, nmae, rmse, nrmse, r, mape, mbe, ss_mae, ss_rmse])
                        csvfile.close()

                else:
                    field_order = ["file_name", "MAE", "nMAE", "RMSE", "nRMSE", "R", "MAPE", "MBE", "SS-MAE", "SS-RMSE"]
                    with open(file_name, 'w', encoding="utf-8", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(field_order)
                        writer.writerow([file_tag, mae, nmae, rmse, nrmse, r, mape, mbe, ss_mae, ss_rmse])
                        csvfile.close()


if __name__ == '__main__':
    main()