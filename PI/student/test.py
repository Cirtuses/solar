import torch
from networkForRegresstion import ResNet50, ResNet152, ResNet50_plain
from torch.utils.data import DataLoader
from dataset import MyDataSet
import numpy as np
from torch import nn
import pandas as pd
import os


def load_model(pre_model_path, model_path, device):
    # net = ResNet152(model_path=pre_model_path)
    net = ResNet50_plain()

    net = net.to(device)
    net.load_state_dict(torch.load(model_path, map_location='cuda:0'))
    # net.load_state_dict(torch.load(model_path, device=device))
    # net = net.to(device)
    net.eval()
    return net


def dateparse(timestamp):
    #   07/21/21 下午06时34分00
    time = pd.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return time


def evaluate_valloss(net, data_iter, label_type, save_path, device=None):
    if isinstance(net, nn.Module):
        net.eval()  # 设置为评估模式
        if not device:
            device = next(iter(net.parameters())).device
    net.eval()
    mse_loss = 0.0
    mae_loss = 0.0
    mbe_loss = 0.0
    mape_loss = 0.0
    all_num = 0.0
    df_result = pd.DataFrame()
    date_list = []
    predict = None
    target_all = None
    with torch.no_grad():
        for X, y, date in data_iter:
            X = X.to(device)
            y = y.to(device)
            if label_type == 'ghi':
                y = y.reshape(-1, 1) * 1000.0
                all_num = all_num + y.numel()
                y_hat = net(X) * 1000.0
            elif label_type == 'dhi':
                y = y.reshape(-1, 1) * 600.0
                all_num = all_num + y.numel()
                y_hat = net(X) * 600.0
            elif label_type == 'dni':
                y = y.reshape(-1, 1) * 800.0
                all_num = all_num + y.numel()
                y_hat = net(X) * 800.0
            if predict is None:
                predict = y_hat
                target_all = y
            else:
                predict = torch.cat((predict, y_hat))
                target_all = torch.cat((target_all, y))
            date_tmp = list(date)
            date_list = date_list + date_tmp
            y = y.cpu().numpy()
            y_hat = y_hat.cpu().numpy()
            y = y
            y_hat = y_hat
            mae_loss = mae_loss + sum(abs(y-y_hat))
            mbe_loss = mbe_loss + sum(y-y_hat)
            mse_loss = mse_loss + sum((y - y_hat)**2)
            mape_loss = mape_loss + sum(abs((y - y_hat) / y))
    mae_loss = mae_loss / all_num
    mbe_loss = mbe_loss / all_num
    mse_loss = mse_loss / all_num
    rmse_loss = np.sqrt(mse_loss)
    mape_loss = (mape_loss / all_num) * 100.0
    mean_p = predict.mean()
    mean_g = target_all.mean()
    sigma_p = predict.std()
    sigma_g = target_all.std()
    correlation = ((predict - mean_p) * (target_all - mean_g)).mean(axis=0) / (sigma_p * sigma_g)
    index = (sigma_g != 0)
    correlation = (correlation[index]).mean()
    predict = predict.cpu().numpy().reshape(-1, )
    target_all = target_all.cpu().numpy().reshape(-1, )
    df_result['Time'] = date_list
    df_result['Time'] = df_result['Time'].map(dateparse)
    if label_type == 'ghi':
        df_result['ghi_target'] = target_all
        df_result['ghi_predict'] = predict
        save_result = save_path + '/' + 'ghi_result.csv'
        df_result.to_csv(save_result, index=None)
    elif label_type == 'dhi':
        df_result['dhi_target'] = target_all
        df_result['dhi_predict'] = predict
        save_result = save_path + '/' + 'dhi_result.csv'
        df_result.to_csv(save_result, index=None)
    elif label_type == 'dni':
        df_result['dni_target'] = target_all
        df_result['dni_predict'] = predict
        save_result = save_path + '/' + 'dni_result.csv'
        df_result.to_csv(save_result, index=None)

    return mae_loss, mbe_loss, mse_loss, rmse_loss, mape_loss, correlation


if __name__ == "__main__":
    torch.cuda.set_device(0)
    # 参数设置
    batch_size = 16
    eval_epochs = 100
    eval_path = '../300I_300H/data/test'
    model_name = 'ClassRes32_ResNet152'
    model_name = 'ResNet50_model'
    pre_model_path = 'solar_resnet32__baseline1_best.pt'
    model_path = '60I_300H/50_ghi/ResNet50_model_7.pt'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data_type = 'ghi'
    save_path = '60I_300H/50_ghi'
    # device = torch.device("cpu")
    test_dataset = MyDataSet(img_path=eval_path, train=False, test=True, target_label=data_type, add_mask=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    net = load_model(pre_model_path=pre_model_path, model_path=model_path, device=device)
    mae_loss, mbe_loss, mse_loss, rmse_loss, mape_loss, correlation = evaluate_valloss(net=net,
                                                                                       data_iter=test_loader,
                                                                                       label_type=data_type,
                                                                                       save_path=save_path,
                                                                                       device=device)
    test_info_file = save_path + '/' + 'test_info.txt'
    file_to_write = open(test_info_file, 'a')
    print("MAE: {} MBE: {} MSE: {} RMSE: {} MAPE: {} Corr: {}".format(
        mae_loss[0], mbe_loss[0], mse_loss[0], rmse_loss[0], mape_loss[0], correlation
    ))
    file_to_write.write("MAE: {} MBE: {} MSE: {} RMSE: {} MAPE: {} Corr: {}\n".format(
        mae_loss[0], mbe_loss[0], mse_loss[0], rmse_loss[0], mape_loss[0], correlation
    ))
    file_to_write.close()

