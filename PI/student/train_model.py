import torch
from torch import nn
import time
from dataset import MyDataSet
from torch.utils.data import DataLoader
import numpy as np
from networkForRegresstion import ResNet50, ResNet152
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = '1'


def train_model(net, train_loader, val_loader, num_epochs, lr, device, save_file, net_name,
                momentum, weight_decay, save_file_path):
    net.to(device)
    optimizer = torch.optim.SGD(net.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
    milestones = [15, 50, 80]
    torch.optim.lr_scheduler.MultiStepLR(optimizer=optimizer, milestones=milestones, gamma=0.1, last_epoch=-1)
    best_loss = 1e8
    # optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    loss = nn.MSELoss()
    for epoch in range(num_epochs):
        time_start = time.time()
        train_loss = 0.0
        all_num = 0.0
        net.train()
        for i, (X, y, date) in enumerate(train_loader):
            optimizer.zero_grad()
            X, y = X.to(device), y.to(device)
            y = y.reshape(-1, 1)
            y_hat = net(X)
            l = loss(y_hat, y)
            l.backward()
            optimizer.step()
            with torch.no_grad():
                train_loss = train_loss + l * X.shape[0]
                all_num = all_num + X.shape[0]
        train_loss = train_loss / all_num
        epoch_time = time.time() - time_start

        mae_loss, mbe_loss, mse_loss, rmse_loss, mape_loss, corr_loss = evaluate_valloss(net, val_loader, device=device)

        if best_loss > mae_loss:
            best_loss = mae_loss
            model_name = save_file_path + '/' + net_name + "_model_{}".format(epoch + 1) + ".pt"
            torch.save(net.state_dict(), model_name)
        print("epoch: {} train loss: {} epoch_time: {} MAE: {} MBE: {} MSE: {} RMSE: {} MAPE: {} Corr: {}".format(
            epoch+1, train_loss, epoch_time, mae_loss[0], mbe_loss[0], mse_loss[0], rmse_loss[0], mape_loss[0], corr_loss
        ))
        save_file.write("epoch: {} train loss: {} epoch_time: {} MAE: {} MBE: {} MSE: {} RMSE: {} MAPE: {} Corr: {}\n".format(
            epoch+1, train_loss, epoch_time, mae_loss[0], mbe_loss[0], mse_loss[0], rmse_loss[0], mape_loss[0], corr_loss
        ))
        # if (epoch + 1) % save_interval == 0:
        #     model_name = net_name + "_model_{}".format(epoch + 1) + ".pt"
        #     torch.save(net.state_dict(), model_name)
        # print("epoch: {} train loss: {} epoch_time: {} train_acc: {} test_acc: {}".format(epoch + 1, train_loss,
        #                                                                                   epoch_time, train_acc,
        #                                                                                   test_acc))
        # save_file.write("epoch: {} train loss: {} epoch_time: {} train_acc: {} test_acc: {}\n".format(
        #     epoch + 1, train_loss, epoch_time, train_acc, test_acc))



def evaluate_valloss(net, data_iter, device=None):
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
    predict = None
    target_all = None
    with torch.no_grad():
        for X, y, date in data_iter:
            X = X.to(device)
            y = y.to(device)
            y = y.reshape(-1, 1)
            all_num = all_num + y.numel()
            y_hat = net(X)
            if predict is None:
                predict = y_hat
                target_all = y
            else:
                predict = torch.cat((predict, y_hat))
                target_all = torch.cat((target_all, y))
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
    return mae_loss, mbe_loss, mse_loss, rmse_loss, mape_loss, correlation


if __name__ == "__main__":




    torch.cuda.set_device(0)
    # 参数设置
    train_info_file = 'result' + '/' + 'train_info.txt'
    file_to_write = open(train_info_file, 'a')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_path = '../60I_300H/data/train'
    train_path = '../300I_300H/data/train'
    load_model_path = 'class/solar_resnet32__baseline1_best.pt'
    val_path = '../300I_300H/data/val'
    data_type = 'ghi'
    # data_type = 'dhi'
    mask = 0
    batch_size = 16
    # batch_size = 8
    epoch = 100
    lr = 0.001
    momentum = 0.90
    weight_decay = 0.01
    model_name = 'ClassRes32_ResNet152'
    save_path = '300I_300H'
    # device = torch.device("cpu")
    time_pre = time.time()
    # 获取数据及数据划分
    train_dataset = MyDataSet(img_path=train_path, train=True, test=False, target_label=data_type, add_mask=mask)
    val_dataset = MyDataSet(img_path=val_path, train=False, test=False, target_label=data_type, add_mask=mask)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    net = ResNet152(model_path=load_model_path)
    train_model(net=net, train_loader=train_loader, val_loader=val_loader, num_epochs=epoch, lr=lr, device=device,
                save_file=file_to_write, net_name=model_name, momentum=momentum, weight_decay=weight_decay,
                save_file_path=save_path)
    file_to_write.close()
    time_all = time.time() - time_pre
    print("Run time is {}".format(time_all))
