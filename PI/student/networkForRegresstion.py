from torch import nn
import torchvision
from torchvision import transforms
from resnet_cifar import resnet32
import torch
import torch.nn.functional as F


class ResNet50(nn.Module):
    def __init__(self, model_path):
        super(ResNet50, self).__init__()
        self.resnet50 = torchvision.models.resnet50(pretrained=True)
        self.resnet50.conv1 = nn.Conv2d(4, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)

        self.net_class = resnet32(num_classes=5)
        self.net_class.load_state_dict(torch.load(model_path,map_location='cpu'))
        self.net_class.eval()

        self.future_map = nn.Linear(5, 480)
        self.fc3 = nn.Linear(1000, 1)

    def forward(self, x):
        with torch.no_grad():
            tmp_trans = transforms.Resize(32)
            tmp_x = tmp_trans(x)
            result1 = self.net_class(tmp_x)
            result1 = F.softmax(result1)
            result1 = result1 / torch.sum(result1, dim=1, keepdim=True)
        tmp_result = self.future_map(result1)
        tmp_result = torch.unsqueeze(tmp_result, -1)
        tmp_result = tmp_result.repeat(1, 1, 480)
        tmp_result = torch.unsqueeze(tmp_result, 1)
        x = torch.cat((x, tmp_result), 1)
        x = self.resnet50(x)
        x = self.fc3(x)
        return x


class ResNet152(nn.Module):
    def __init__(self, model_path):
        super(ResNet152, self).__init__()
        self.resnet152 = torchvision.models.resnet152(pretrained=True)
        self.resnet152.conv1 = nn.Conv2d(4, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)

        self.net_class = resnet32(num_classes=5)
        self.net_class.load_state_dict(torch.load(model_path))
        self.net_class.eval()

        self.future_map = nn.Linear(5, 480)
        self.fc3 = nn.Linear(1000, 1)

    def forward(self, x):
        with torch.no_grad():
            tmp_trans = transforms.Resize(32)
            tmp_x = tmp_trans(x)
            result1 = self.net_class(tmp_x)
            result1 = F.softmax(result1)
            result1 = result1 / torch.sum(result1, dim=1, keepdim=True)
        tmp_result = self.future_map(result1)
        tmp_result = torch.unsqueeze(tmp_result, -1)
        tmp_result = tmp_result.repeat(1, 1, 480)
        tmp_result = torch.unsqueeze(tmp_result, 1)
        x = torch.cat((x, tmp_result), 1)
        x = self.resnet152(x)
        x = self.fc3(x)
        return x


if __name__ == "__main__":
    from torchstat import stat
    import torchvision.models as models
    model = models.resnet18()
    model = models.mobilenet_v2()
    # model = resnet32()

    # inputs = (3, 480, 480)
    # # (3, 480, 480)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # inputs = inputs.to(device)
    # stat(model, (3, 480, 480))
    stat(model, (3, 32, 32))
    exit()



class ResNet50_plain(nn.Module):
    def __init__(self):
        super(ResNet50_plain, self).__init__()
        self.resnet50_plain = torchvision.models.resnet50(pretrained=True)
        self.fc3 = nn.Linear(1000, 1)

    def forward(self, x):
        x = self.resnet50_plain(x)
        x = self.fc3(x)
        return x