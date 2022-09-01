import torch
from torch import nn
import time
from dataset import MyDataSet
from torch.utils.data import DataLoader
import numpy as np
from config import parsers
from ResNet50 import ResNet50
from ResNet152 import ResNet152


"""
Function for model training

    net: Model used
    train_loader: Training set
    val_loader: Validation set
    num_epochs: Training rounds
    lr: learning rate
    device: Equipment used in the training (CPU or GPU)
    save_file: File to store training information
    net_name: Model name used
    momentum: Momentum value
    weight_decay: Parameters for weight decay
    save_file_path: Path to save training results
"""
def train_model(net, train_loader, val_loader, num_epochs, lr, device, save_file, net_name,
                momentum, weight_decay, save_file_path):
    net.to(device)
    optimizer = torch.optim.SGD(net.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
    # Learning rate decay
    milestones = [15, 50, 80]
    torch.optim.lr_scheduler.MultiStepLR(optimizer=optimizer, milestones=milestones, gamma=0.1, last_epoch=-1)
    best_loss = 1e8

    # Using mean square error loss
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

        # Use the validation set to evaluate the training result
        mae_loss, mbe_loss, mse_loss, rmse_loss, mape_loss, corr_loss = evaluate_valloss(net, val_loader, device=device)

        # Store the best performing model parameters in the validation set
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



"""
    The tag value predicted by the model is compared with the real value 
    to calculate each evaluation index

        net: Model used
        data_iter: Data sets to be evaluated
        device: Equipment used in the evaluation (CPU or GPU)
"""
def evaluate_valloss(net, data_iter, device=None):
    if isinstance(net, nn.Module):
        net.eval()  # Set to evaluation mode
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
    opt = parsers()
    # Parameter setting
    train_info_file = opt.save_path + '/' + 'train_info.txt'
    file_to_write = open(train_info_file, 'a')

    # Training with GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    time_pre = time.time()

    # Data acquisition and data division
    train_dataset = MyDataSet(img_path=opt.train_path, train=True, target_label=opt.data_type, add_mask=opt.mask)
    val_dataset = MyDataSet(img_path=opt.val_path, train=False, target_label=opt.data_type, add_mask=opt.mask)
    train_loader = DataLoader(train_dataset, batch_size=opt.batch_size, shuffle=True, num_workers=opt.num_workers)
    val_loader = DataLoader(val_dataset, batch_size=opt.batch_size, shuffle=False, num_workers=opt.num_workers)

    net = None
    # Select model architecture
    if opt.model_name == 'ResNet152':
        net = ResNet152()
    elif opt.model_name == 'ResNet50':
        net = ResNet50()

    # Start training
    train_model(net=net, train_loader=train_loader, val_loader=val_loader, num_epochs=opt.epoch, lr=opt.lr, device=device,
                save_file=file_to_write, net_name=opt.model_name, momentum=opt.momentum, weight_decay=opt.weight_decay,
                save_file_path=opt.save_path)
    file_to_write.close()
    time_all = time.time() - time_pre
    print("Run time is {}".format(time_all))
