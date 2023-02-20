import os
import matplotlib.pyplot as plt


def plot_comp(mae, rmse, mape, r2, save_flag, save_name):
    fig = plt.figure(figsize=(12, 9), dpi=100)
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    x_ticks = ['10I_300H', '60I_300H', '300I_300H']

    
    # fig = plt.figure()
    
    ax1 = fig.add_subplot(111)
  
    
    ax1.plot(x_ticks, mae, c='red', label="MAE")
    ax1.plot(x_ticks, rmse, c='green', linestyle='--', label="RMSE")
    ax1.plot(x_ticks, r2, c='yellow', linestyle='--', label="RMSE")

    
    ax1.scatter(x_ticks, mae, c='red')
    ax1.scatter(x_ticks, rmse, c='green')
    ax1.scatter(x_ticks, r2, c='yellow')

    plt.legend(loc='best')
    
    ax2 = ax1.twinx() 
    ax2.plot(x_ticks, mape, c='blue', linestyle='-.', label="MAPE")
    ax2.scatter(x_ticks, mape, c='blue')
    
    plt.legend(loc='best')
    
    ax1.set_yticks(range(80, 160, 5))
    ax2.set_yticks(range(0, 50, 5))
    
    # ax1.set_xticks([0.5,  1, 1.5], x_ticks, fontsize=14)
    
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("任务类型", fontdict={'size': 16})
    ax1.set_ylabel("RMSE MAE", fontdict={'size': 16})
    ax2.set_ylabel("MAPE(%)", fontdict={'size': 16})
    plt.title("GHI指标对比", fontdict={'size': 20})
    plt.savefig(os.path.join('comp', save_name), bbox_inches='tight')
    plt.show()

    


if __name__ == '__main__':
    '''
    GHI 300H
        mae = [92.37, 94.39, 100.47]
        rmse = [147.21, 144.36, 151.39]
        mape = [23.13, 13.51, 25.70]
        r2 = [0.8832, 0.8839, 0.8733]
    '''
    
    mae = [92.37, 94.39, 100.47]
    rmse = [147.21, 144.36, 151.39]
    mape = [23.13, 13.51, 25.70]
    r2 = [0.8832, 0.8839, 0.8733]

    save_flag = False
    save_name = '300H_comp.tiff'
    plot_comp(mae, rmse, mape, r2, save_flag, save_name)