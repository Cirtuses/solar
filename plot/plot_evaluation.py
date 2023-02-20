import os
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import matplotlib.pyplot as plt
import numpy as np

def plot_comp(x_label, x_xticks_name, ylim_dict , mae, rmse, mape, r2, save_flag, save_name):
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    
    fig = plt.figure(1, figsize=(12, 6))  # 定义figure，（1）中的1是什么
    ax_cof = HostAxes(fig, [0.08, 0.08, 0.65, 0.9])  # 用[left, bottom, weight, height]的方式定义axes，0 <= l,b,w,h <= 1

    # parasite addtional axes, share x
    ax_temp = ParasiteAxes(ax_cof, sharex=ax_cof)
    ax_load = ParasiteAxes(ax_cof, sharex=ax_cof)
    ax_cp = ParasiteAxes(ax_cof, sharex=ax_cof)
    # ax_wear = ParasiteAxes(ax_cof, sharex=ax_cof)


    # append axes
    ax_cof.parasites.append(ax_temp)
    ax_cof.parasites.append(ax_load)
    ax_cof.parasites.append(ax_cp)
    # ax_cof.parasites.append(ax_wear)

    # invisible right axis of ax_cof
    ax_cof.axis['right'].set_visible(False)
    ax_cof.axis['top'].set_visible(False)
    ax_temp.axis['right'].set_visible(True)
    ax_temp.axis['right'].major_ticklabels.set_visible(True)
    ax_temp.axis['right'].label.set_visible(True)

    # set label for axis
    ax_cof.set_ylabel('r')
    # ax_cof.set_xlabel('Distance (m)')
    ax_temp.set_ylabel('MAPE(%)')
    ax_load.set_ylabel('MAE')
    ax_cp.set_ylabel('RMSE')
    # ax_cp.set_ylabel('R$^{2}$')


    load_axisline = ax_load.get_grid_helper().new_fixed_axis
    cp_axisline = ax_cp.get_grid_helper().new_fixed_axis
    # wear_axisline = ax_wear.get_grid_helper().new_fixed_axis

    ax_load.axis['right2'] = load_axisline(loc='right', axes=ax_load, offset=(50, 0))
    ax_cp.axis['right3'] = cp_axisline(loc='right', axes=ax_cp, offset=(100, 0))
    # ax_wear.axis['right4'] = wear_axisline(loc='right', axes=ax_wear, offset=(150, 0))

    fig.add_axes(ax_cof)

    ''' #set limit of x, y
    ax_cof.set_xlim(0,2)
    ax_cof.set_ylim(0,3)
    '''

    
    curve_cof, = ax_cof.plot(x_label, r2, linestyle='--',  label="r", color='black')
    curve_temp, = ax_temp.plot(x_label, mape, linestyle='--', label="MAPE", color='red')
    curve_load, = ax_load.plot(x_label, mae, linestyle='--', label="MAE", color='green')
    curve_cp, = ax_cp.plot(x_label, rmse, linestyle='--', label="RMSE", color='blue')
    
    ax_cof.scatter(x_label, r2, c='black')
    ax_temp.scatter(x_label, mape, c='red')
    ax_load.scatter(x_label, mae, c='green')
    ax_cp.scatter(x_label, rmse, c='blue')


    # ax_cof.set_xticks([0, 1, 2], ['10I_300H', '60I_300H', '300I_300H'], rotation=90, fontsize=7)
    ax_cof.set_xticks(x_label, x_xticks_name)
    ax_cof.set_xlim(-0.2, 1.2)
    
    
    ax_cof.set_ylim(ylim_dict['r2'][0], ylim_dict['r2'][1]) 
    

    ax_temp.set_ylim(ylim_dict['mape'][0], ylim_dict['mape'][1])# MAPE
    ax_load.set_ylim(ylim_dict['mae'][0], ylim_dict['mae'][1])# RMSE
    ax_cp.set_ylim(ylim_dict['rmse'][0], ylim_dict['rmse'][1])  # R2




    ax_cof.legend()

    # 轴名称，刻度值的颜色
    # ax_cof.axis['left'].label.set_color(ax_cof.get_color())
    ax_temp.axis['right'].label.set_color('red')
    ax_load.axis['right2'].label.set_color('green')
    ax_cp.axis['right3'].label.set_color('blue')
    # ax_wear.axis['right4'].label.set_color('blue')

    ax_temp.axis['right'].major_ticks.set_color('red')
    ax_load.axis['right2'].major_ticks.set_color('green')
    ax_cp.axis['right3'].major_ticks.set_color('blue')
    # ax_wear.axis['right4'].major_ticks.set_color('blue')

    ax_temp.axis['right'].major_ticklabels.set_color('red')
    ax_load.axis['right2'].major_ticklabels.set_color('green')
    ax_cp.axis['right3'].major_ticklabels.set_color('blue')
    # ax_wear.axis['right4'].major_ticklabels.set_color('blue')

    ax_temp.axis['right'].line.set_color('red')
    ax_load.axis['right2'].line.set_color('green')
    ax_cp.axis['right3'].line.set_color('blue')
    # ax_wear.axis['right4'].line.set_color('blue')
    # plt.title("GHI指标对比", fontdict={'size': 10})
    
    # ax_cof.set_title("300H GHI指标对比")
    
    if save_flag == True:
        plt.savefig(os.path.join('comp', save_name), dpi=300)

    plt.show()
    
if __name__ == '__main__':
    
    '''
    GHI 60H
    # 10I 60I
    mae = [60.48, 58.82]
    rmse = [97.77, 98.66]
    mape = [13.40, 13.53]
    r2 = [0.949, 0.9481]
    
    ylim_dict = {'mae': [58, 61], 'mape': [13, 14], 'rmse': [97, 99], 'r2': [0.945, 0.95]}
    '''
    
    '''
    DHI 60H
        mae = [20.06, 19.17]
        rmse = [27.75, 27.51]
        mape = [7.64, 7.54]
        r2 = [0.9769, 0.9782]
        
        ylim_dict = {'mae': [18, 21], 'mape': [7, 8], 'rmse': [27, 28], 'r2': [0.975, 0.979]}
    '''
    
    '''
    DNI 60H
    # 10I 60I 300I
        mae = [63.9, 62.74]
        rmse = [104.27, 106.61]
        mape = NULL
        r2 = [0.9353, 0.9324]
        
        ylim_dict = {'mae': [62, 65], 'mape': [10, 26.5], 'rmse': [103, 108], 'r2': [0.93, 0.937]}
    '''

    '''
    GHI 300H
    # 10I 60I 300I
        mae = [92.37, 94.39, 100.47]
        rmse = [147.21, 144.36, 151.39]
        mape = [23.13, 13.51, 25.70]
        r2 = [0.8832, 0.8839, 0.8733]
        
        ylim_dict = {'mae': [90, 104], 'mape': [12, 28], 'rmse': [142, 154], 'r2': [0.87, 0.89]}
    '''
    
    '''
    DHI 300H
    
    mae = [34.21, 33.99, 33.3]
    rmse = [51.36, 49.21, 49.69]
    mape = [12.29, 14.53, 13.07]
    r2 = [0.9198, 0.9231, 0.9221]
    
    ylim_dict = {'mae': [33, 35], 'mape': [12, 15], 'rmse': [48, 52], 'r2': [0.91, 0.93]}
    '''
    
    '''
    DNI 300H
        mae = [106.2, 97.47, 114.61]
        rmse = [157.38, 147.98, 163.56]
        mape = NULL
        r2 = [0.8598, 0.8648, 0.8346]
        
        ylim_dict = {'mae': [90, 102], 'mape': [10, 26.5], 'rmse': [142, 152], 'r2': [0.87, 0.885]}
    '''
    
    
    '''
    GHI 600H
    #10I 60I 300I 600H
    mae = [107.85, 104.42, 114.82, 114.52]
    rmse = [156.33, 164.71, 163.32, 161.37]
    mape = [26.21, 27.01, 30.09, 26.12]
    r2 = [0.8657, 0.8585, 0.8503, 0.8633]
    
    ylim_dict = {'mae': [102, 118], 'mape': [25, 32], 'rmse': [154, 168], 'r2': [0.84, 0.88]}
    '''
    
    '''
    DHI 600H
    mae = [44.1, 42.37, 44.02, 45.92]
    rmse = [60.71, 61.09, 60.83, 63.66]
    mape = [19.05, 17.22, 17.20, 18.37]
    r2 = [0.8867, 0.8785, 0.8844, 0.872]
    
    ylim_dict = {'mae': [42, 47], 'mape': [16, 20], 'rmse': [60, 65], 'r2': [0.87, 0.89]}
    '''

    '''
    DHI 600H
        mae = [115.78, 113.98, 130.19, 115.28]
        rmse = [164.83, 176.24, 180.01, 164.56]
        mape = NULL
        r2 = [0.8372, 0.8203, 0.7976, 0.8335]
        
        ylim_dict = {'mae': [90, 102], 'mape': [10, 26.5], 'rmse': [142, 152], 'r2': [0.87, 0.885]}
    '''
   

    mae = [20.06, 19.17]
    rmse = [27.75, 27.51]
    mape = [7.64, 7.54]
    r2 = [0.9769, 0.9782]
    
    ylim_dict = {'mae': [18, 21], 'mape': [7, 8], 'rmse': [27, 28], 'r2': [0.975, 0.979]}



    
    #ax_cof.set_ylim(91.5, 101.5) # MAE

    save_flag = True
    save_name = '60H_DHI_comp.tiff'
    
    x_label = [0, 1]
    x_xticks_name = ['10I_60H', '60I_60H']
    
   
    
    plot_comp(x_label, x_xticks_name, ylim_dict, mae, rmse, mape, r2, save_flag, save_name)