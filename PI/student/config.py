import argparse


def parsers():
    parser = argparse.ArgumentParser("irradiance prediction")

    # 是否加mask
    parser.add_argument('--mask', type=int, default=0, help='add mask ?')

    # 计算原始训练集的均值和标准差
    parser.add_argument('--cal_mean_std_path', type=str, default='/home/sda4/data/0min-300s-regular/DNI/LR/train',
                        help='path for calculating mean and standard deviation')

    # 划分训练、验证、测试集
    parser.add_argument('--source_train_path', type=str, default='/home/sda4/data/0min-300s-regular/DNI/LR/train',
                        help='path of original training set')
    parser.add_argument('--source_test_path', type=str, default='/home/sda4/data/0min-300s-regular/DNI/LR/test',
                        help='path of original test set')
    parser.add_argument('--target_train_path', type=str, default='data/train', help='target path of train dataset')
    parser.add_argument('--target_val_path', type=str, default='data/val', help='target path of validation dataset')
    parser.add_argument('--target_test_path', type=str, default='data/test', help='target path of test dataset')

    # 设置训练集、验证集、测试集路径
    parser.add_argument('--train_path', type=str, default='data/train', help='path of train dataset')
    parser.add_argument('--val_path', type=str, default='data/val', help='path of validation dataset')
    parser.add_argument('--test_path', type=str, default='data/test', help='path of test dataset')

    # 设置训练和测试的标签类型 ghi、dhi、dni
    parser.add_argument('--data_type', type=str, default='ghi', help='data type')

    # 模型的名称
    parser.add_argument('--model_name', type=str, default='ResNet152', help='model name that will be used')

    # 模型和结果保存路径
    parser.add_argument('--save_path', type=str, default='result', help="the save path of result")

    # 模型加载路径
    parser.add_argument('--load_model', type=str, default='result/ResNet152_model_86.pt', help='the load model path')

    # 训练设置
    parser.add_argument('--epoch', type=int, default=100, help='train epoches')
    parser.add_argument('--batch_size', type=int, default=16, help='batch size')
    parser.add_argument('--num_workers', type=int, default=0, help='number of cpus to train')

    # 优化器设置
    parser.add_argument('--lr', type=float, default=0.001, help='learning rate of model')
    parser.add_argument('--momentum', type=float, default=0.90, help='momentum of learning')
    parser.add_argument('--weight_decay', type=float, default=0.01, help='regularization parameter')

    # 预测某张图片的辐射值：图片路径
    parser.add_argument('--predict_img', type=str, help='Path of a picture to be predicted')

    args = parser.parse_args()
    return args
