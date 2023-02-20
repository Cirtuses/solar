import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == '__main__':
    data_key = '60_300'
    target_type = 'ghi'
    p_model = False
    read_path = 'D:/solar/solar/class_res/60I-300H152/ghi_result.csv'
    save_path = 'D:/solar/solar/picture/p-model/'
    
    if not os.path.exists(save_path):
        # train_path = os.path.join(dst_path, "train")
        # test_path = os.path.join(dst_path, "test")
        os.makedirs(save_path)
        # os.makedirs(test_path)

    df_data = pd.read_csv(read_path)
    dateAllList = list(df_data['Time'].values)

    date_interval_dict = {}
    time_interval_dict = {}
    tick_interval_dict = {}
    date_interval_dict['10_300'] = 3031
    time_interval_dict['10_300'] = 30
    date_interval_dict['300_300'] = 102
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

    # if time_interval == 60:
    #     if cuowei == 0:
    #         date_interval = 511
    #         tick_interval = 30
    #     else:
    #         date_interval = 510
    #         tick_interval = 30
    # elif time_interval == 600:
    #     if cuowei == 0:
    #         date_interval = 52
    #         tick_interval = 3
    #     else:
    #         date_interval = 51
    #         tick_interval = 3
    # elif time_interval == 300:
    #     if cuowei == 0:
    #         date_interval = 103
    #         tick_interval = 6
    #     else:
    #         # date_interval = 102
    #         date_interval = 97
    #         tick_interval = 6
    # else:
    #     if cuowei == 0:
    #         date_interval = 3061
    #         tick_interval = 180
    #     else:
    #         # date_interval = 3060
    #         date_interval = 3031
    #         tick_interval = 180

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
    for i in range(len(dateList)):
        date_target_dict[dateList[i]] = data_target[date_index_list[i]:date_index_list[i + 1]]
        date_predict_dict[dateList[i]] = data_predict[date_index_list[i]:date_index_list[i + 1]]
        tmp_ps = list(date_target_dict[dateList[i]])
        aaa = len(tmp_ps)
        del tmp_ps[aaa - num_del:aaa]
        # tmp = tmp_ps[0]
        # tmp_ps.insert(0, tmp)
        # tmp_ps.pop()
        date_persistence_dict[dateList[i]] = np.array(tmp_ps)
        # a = sum(abs(date_persistence_dict[dateList[i]] - date_target_dict[dateList[i]]))
        # b = 1

    # date_plot_list = ['2021-5-22', '2021-5-9', '2021-5-30', '2021-4-25', '2021-6-21', '2021-6-25',
    #                   '2021-7-1', '2021-5-20']
    date_plot_list = ['2021-4-25', '2021-5-9', '2021-5-20', '2021-5-22', '2021-5-30', '2021-6-21',
                      '2021-6-25', '2021-7-1']

    x = [tmp for tmp in range(len(date_target_dict['2021-5-22']))]
    x_pModel = [tmp for tmp in range(num_del, len(date_target_dict['2021-5-22']))]

    ticks = [tmp for tmp in range(0, len(date_target_dict['2021-5-22']), tick_interval)]

    date_tmp_list = dateAllList[0:date_interval]
    x_tick_labels = [date_tmp_list[j].split(' ')[-1][0:5] for j in ticks]

    fig, axs = plt.subplots(4, 2, figsize=(12, 13))
    ax = []
    for i in range(4):
        for j in range(2):
            ax.append(axs[i, j])
    for i in range(8):
        ax[i].plot(x, date_target_dict[date_plot_list[i]], label='Measurement', linewidth=0.8)
        ax[i].plot(x, date_predict_dict[date_plot_list[i]], label='Nowcasting', linewidth=0.8)
        if p_model:
            ax[i].plot(x_pModel, date_persistence_dict[date_plot_list[i]], label='Persistence', linewidth=0.8)
        ax[i].set_ylim(0, y_max_lim)
        # if i % 2 == 0:
        #     yTmpName = yName + ' [W/' + "$m^2$" + ']'
        #     ax[i].set_ylabel(yTmpName)
        yTmpName = yName + ' [W/' + "$m^2$" + ']'
        ax[i].set_ylabel(yTmpName)
        # tmp_title = date_plot_list[i] + ' (' + date_weather_dict[date_plot_list[i]] + ')'
        tmp_title = date_plot_list[i]
        ax[i].set_title(tmp_title, fontsize=10)
        ax[i].set_xticks(ticks, x_tick_labels, rotation=90, fontsize=10)
        ax[i].set_yticks(yTicks, y_tick_labels, fontsize=10)
        ax[i].grid()
        ax[i].legend(fontsize=10, loc='upper right')

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.15, hspace=0.32, left=0.08, top=0.96)

    filesavename = save_path + data_key + '_' + target_type + '.jpg'
    fig.savefig(filesavename, dpi=300)

    # plt.savefig(filesavename, dpi=600)
