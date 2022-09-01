import argparse


def parsers():
    # Parameter setting
    parser = argparse.ArgumentParser("irradiance prediction")

    # Whether to add mask
    parser.add_argument('--mask', type=int, default=0, help='add mask ?')

    # Calculate the mean and standard deviation of the original training set
    parser.add_argument('--cal_mean_std_path', type=str, default='/home/sda4/data/0min-300s-regular/DNI/LR/train',
                        help='path for calculating mean and standard deviation')

    # The original data set is divided into training, verification and test sets
    parser.add_argument('--source_train_path', type=str, default='/home/sda4/data/0min-300s-regular/DNI/LR/train',
                        help='path of original training set')
    parser.add_argument('--source_test_path', type=str, default='/home/sda4/data/0min-300s-regular/DNI/LR/test',
                        help='path of original test set')
    parser.add_argument('--target_train_path', type=str, default='data/train', help='target path of train dataset')
    parser.add_argument('--target_val_path', type=str, default='data/val', help='target path of validation dataset')
    parser.add_argument('--target_test_path', type=str, default='data/test', help='target path of test dataset')

    # Set the path of training set, verification set and test set
    parser.add_argument('--train_path', type=str, default='data/train', help='path of train dataset')
    parser.add_argument('--val_path', type=str, default='data/val', help='path of validation dataset')
    parser.add_argument('--test_path', type=str, default='data/test', help='path of test dataset')

    # Set the tag types of training and testing (GHI, DHI, DNI)
    parser.add_argument('--data_type', type=str, default='ghi', help='data type')

    # Name of the model
    parser.add_argument('--model_name', type=str, default='ResNet152', help='model name that will be used')

    # Model and result saving path
    parser.add_argument('--save_path', type=str, default='result', help="the save path of result")

    # Model loading path
    parser.add_argument('--load_model', type=str, default='result/ResNet152_model_86.pt', help='the load model path')

    # Training settings
    parser.add_argument('--epoch', type=int, default=100, help='train epoches')
    parser.add_argument('--batch_size', type=int, default=16, help='batch size')
    parser.add_argument('--num_workers', type=int, default=0, help='number of cpus to train')

    # Optimizer settings
    parser.add_argument('--lr', type=float, default=0.001, help='learning rate of model')
    parser.add_argument('--momentum', type=float, default=0.90, help='momentum of learning')
    parser.add_argument('--weight_decay', type=float, default=0.01, help='regularization parameter')

    args = parser.parse_args()
    return args
