import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


allday_flag = False
dateList = ['2021-4-25', '2021-5-9', '2021-5-20', '2021-5-22', '2021-5-30', '2021-6-21', '2021-6-25', '2021-7-1']
date = dateList[1]
data_key = '60_300'
target_type = 'ghi'
p_model = True
read_path = r'D:\solar\target\60I_300H(student)\60I_300H(0.3)\ghi_result.csv'
read_path = r'D:\solar\solar\class_res\60I_300H(32+152)\ghi_result.csv'

baseline_path = r'D:\solar\target\60I_300H(SSM152)\ghi_result.csv' #需要比较的其他方法
# baseline_path = r'D:\solar\solar\class_res\60I_300H(50)\ghi_result.csv'

save_path = r'D:\solar\solar\picture\60I_300H(0.3)'
save_path = os.path.join(save_path)

if p_model == True:
    save_path = os.path.join(save_path, 'with_p-model')
else:
    save_path = os.path.join(save_path, 'no_p-model')
    

def oneday(dateAllList, num_del, date_target_dict, date_predict_dict, date_persistence_dict ,data_baselinepredict_dict, date, date_interval, tick_interval, y_max_lim, x_max_lim):
    x = [tmp for tmp in range(len(date_target_dict['2021-5-22']))]
    
    x_pModel = [tmp for tmp in range(num_del, len(date_target_dict['2021-5-22']))]

    ticks = [tmp for tmp in range(0, len(date_target_dict['2021-5-22']), tick_interval)]
    # if cuowei == 0:
    #     ticks = [tmp for tmp in range(0, len(date_target_dict['2021-5-22']), tick_interval)]
    # else:
    #     ticks = [tmp for tmp in range(tick_interval-1, len(date_target_dict['2021-5-22']), tick_interval)]
    date_tmp_list = dateAllList[0:date_interval]

    x_tick_labels = [date_tmp_list[j].split(' ')[-1][0:5] for j in ticks]
    # print(x_tick_labels)
    # exit()
    
    # print(date_target_dict[date])
    # exit()
    
    plt.figure(figsize=(12, 6))
    plt.plot(x, date_target_dict[date], label='Measurement', linewidth=1.2, color = 'C0')
    # plt.plot(x, data_baselinepredict_dict[date], label='SSM152', linewidth=1, color = 'g')
    # plt.plot(x, date_predict_dict[date], label='DSMT', linewidth=1, color = 'y')
    if p_model:
        plt.plot(x_pModel, date_persistence_dict[date], label='P model', linewidth=1.2, color = 'C1')
    plt.plot(x, data_baselinepredict_dict[date], label='SSM152', linewidth=1.2, color = 'C2')
    plt.plot(x, date_predict_dict[date], label='DSMT', linewidth=1.2, color = 'purple') #C6
    

    plt.ylim(0, y_max_lim)
    plt.xlim(0, x_max_lim)
    yTmpName = yName + ' (W/' + "$m^2$" + ')'
    plt.ylabel(yTmpName, fontsize=11)
    plt.title(date, fontsize=11)
    plt.xticks(ticks, x_tick_labels, rotation=45, fontsize=10)
    plt.yticks(yTicks, y_tick_labels, fontsize=10)
    plt.grid()
    plt.legend()
    picture_name = date + '_' + target_type + '.tiff'
    filesavename = os.path.join(save_path, picture_name) 
    
    print(filesavename)
    plt.savefig(filesavename, dpi=400)
    # plt.show()
    
    
def allday(dateAllList, date_target_dict, date_plot_list):
    
    x = [tmp for tmp in range(len(date_target_dict['2021-5-22']))]
    
    x_pModel = [tmp for tmp in range(num_del, len(date_target_dict['2021-5-22']))]

    ticks = [tmp for tmp in range(0, len(date_target_dict['2021-5-22']), tick_interval)]
    date_tmp_list = dateAllList[0:date_interval]
    x_tick_labels = [date_tmp_list[j].split(' ')[-1][0:5] for j in ticks]
    
    fig, axs = plt.subplots(2, 4, figsize=(22, 5))
    ax = []
    for i in range(2):
        for j in range(4):
            ax.append(axs[i, j])
    for i in range(8):
        ax[i].plot(x, date_target_dict[date_plot_list[i]], label='Measurement', linewidth=0.8)
        ax[i].plot(x, date_predict_dict[date_plot_list[i]], label='Nowcasting', linewidth=0.8)
        if p_model:
            ax[i].plot(x_pModel, date_persistence_dict[date_plot_list[i]], label='Persistence', linewidth=0.8)
        ax[i].set_ylim(0, y_max_lim)
        if i == 0 or i == 4:
            yTmpName = yName + ' [W/' + "$m^2$" + ']'
            ax[i].set_ylabel(yTmpName)
        tmp_title = date_plot_list[i]
        ax[i].set_title(tmp_title, fontsize=7)
        ax[i].set_xticks(ticks, x_tick_labels, rotation=90, fontsize=7)
        ax[i].set_yticks(yTicks, y_tick_labels, fontsize=7)
        ax[i].grid()
        ax[i].legend(fontsize=7, loc='upper right')
    
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.15, hspace=0.35, left=0.05)

    filesavename = os.path.join(save_path , data_key + '_' + target_type + '.tiff') 
    fig.savefig(filesavename, dpi=300)


if __name__ == '__main__':
    
    if not os.path.exists(save_path):
        # train_path = os.path.join(dst_path, "train")
        # test_path = os.path.join(dst_path, "test")
        os.makedirs(save_path)

    # prefix_name = 'resnet152_Interval-10s_horizon-300s'
    # time_interval = 10
    # cuowei = 1
    base_data = pd.read_csv(baseline_path)
    df_data = pd.read_csv(read_path)
    dateAllList = list(df_data['Time'].values)

    date_interval_dict = {}
    time_interval_dict = {}
    tick_interval_dict = {}
    date_interval_dict['10_300'] = 3031
    time_interval_dict['10_300'] = 30
    date_interval_dict['300_300'] = 101
    time_interval_dict['300_300'] = 1
    date_interval_dict['10_10'] = 3060
    time_interval_dict['10_10'] = 1
    date_interval_dict['10_60'] = 3055
    time_interval_dict['10_60'] = 6
    date_interval_dict['60_60'] = 510
    time_interval_dict['60_60'] = 1
    date_interval_dict['60_300'] = 506
    time_interval_dict['60_300'] = 5
    date_interval_dict['10_600'] = 3001
    time_interval_dict['10_600'] = 60
    date_interval_dict['60_600'] = 501
    time_interval_dict['60_600'] = 10
    date_interval_dict['300_600'] = 101
    time_interval_dict['300_600'] = 2
    date_interval_dict['600_600'] = 51
    time_interval_dict['600_600'] = 1

    tick_interval_dict['10_300'] = 180
    tick_interval_dict['10_10'] = 180
    tick_interval_dict['10_60'] = 180
    tick_interval_dict['60_60'] = 30
    tick_interval_dict['60_300'] = 30
    tick_interval_dict['300_300'] = 6
    tick_interval_dict['10_600'] = 180
    tick_interval_dict['60_600'] = 30
    tick_interval_dict['300_600'] = 6
    tick_interval_dict['600_600'] = 3

    if target_type == 'ghi':
        yName = 'GHI'
        y_max_lim = 1400
        data_target = df_data['ghi_target'].values
        data_predict = df_data['ghi_predict'].values
        
        data_baseline_predict = base_data['ghi_predict'].values
        
        yTicks = [y_i for y_i in range(0, 1500, 200)]
        y_tick_labels = [str(y_i) for y_i in yTicks]
    elif target_type == 'dhi':
        yName = 'DHI'
        y_max_lim = 800
        data_target = df_data['dhi_target'].values
        data_predict = df_data['dhi_predict'].values
        yTicks = [y_i for y_i in range(0, 850, 200)]
        y_tick_labels = [str(y_i) for y_i in yTicks]
    else:
        yName = 'DNI'
        y_max_lim = 1000
        data_target = df_data['dni_target'].values
        data_predict = df_data['dni_predict'].values
        data_predict[data_predict < 0] = 0.0
        yTicks = [y_i for y_i in range(0, 1100, 200)]
        y_tick_labels = [str(y_i) for y_i in yTicks]

    date_interval = date_interval_dict[data_key]
    tick_interval = tick_interval_dict[data_key]
    num_del = time_interval_dict[data_key]

    dateList = ['2021-4-25', '2021-5-9', '2021-5-20', '2021-5-22', '2021-5-30', '2021-6-21', '2021-6-25', '2021-7-1']
    weatherList = ['Overcast', 'Cloudy', 'Overcast', 'Clear', 'Cloudy', 'Clear', 'Cloudy', 'Cloudy']
    date_weather_dict = {}
    for i in range(len(dateList)):
        date_weather_dict[dateList[i]] = weatherList[i]
    date_index_list = []
    cal_tmp_date = 0
    for i in range(8):
        date_index_list.append(cal_tmp_date)
        cal_tmp_date = cal_tmp_date + date_interval
    date_index_list.append(cal_tmp_date)
    del cal_tmp_date

    date_target_dict = {}
    date_predict_dict = {}
    date_persistence_dict = {} 
    data_baselinepredict_dict = {} #存放数据
    
    for i in range(len(dateList)):
        date_target_dict[dateList[i]] = data_target[date_index_list[i]:date_index_list[i + 1]]
        date_predict_dict[dateList[i]] = data_predict[date_index_list[i]:date_index_list[i + 1]]
        
        data_baselinepredict_dict[dateList[i]] = data_baseline_predict[date_index_list[i]:date_index_list[i + 1]]
        
        tmp_ps = list(date_target_dict[dateList[i]])
        aaa = len(tmp_ps)
        del tmp_ps[aaa - num_del:aaa]
        # tmp = tmp_ps[0]
        # tmp_ps.insert(0, tmp)
        # tmp_ps.pop()
        date_persistence_dict[dateList[i]] = np.array(tmp_ps)
        # a = sum(abs(date_persistence_dict[dateList[i]] - date_target_dict[dateList[i]]))
        # b = 1
        
    date_plot_list = ['2021-4-25', '2021-5-9', '2021-5-20', '2021-5-22', '2021-5-30', '2021-6-21',
                      '2021-6-25', '2021-7-1']
    x_max_lim = date_interval_dict[data_key] 
    if allday_flag == True:
        allday(dateAllList, date_target_dict, date_plot_list)
    else:
        dateList = ['2021-4-25', '2021-5-9', '2021-5-20', '2021-5-22', '2021-5-30', '2021-6-21', '2021-6-25', '2021-7-1']
        for date in dateList:
            oneday(dateAllList, num_del, date_target_dict, date_predict_dict, date_persistence_dict, data_baselinepredict_dict ,date, date_interval, tick_interval, y_max_lim, x_max_lim)


