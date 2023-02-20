import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dir_path=r"D:\solar\solar\plot\sim"

def dateparse(timestamp):
    return pd.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

def read(file_path):
    MS = 'Cooling' 

    TIME = 'TMSTAMP'
    T = 'Temperature'
    print(file_path)
    exit()
    data = pd.read_csv(file_path, usecols = [MS, TIME, T],parse_dates=[TIME], date_parser=dateparse, sep=' ', header = 1) # 从csv文件中读出对应的列
    print(data)
    
def main():
    
    read(os.path.join(dir_path, 'measure.txt'))
    # dir_path = r"D:/solar/solar/20211018/20211018.csv"
    # calculate_dni_from_onefile(dir_path, True)


if __name__ == "__main__":
    main()
