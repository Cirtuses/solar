from torch import nn
import torchvision


class ResNet152(nn.Module):
    def __init__(self):
        super(ResNet152, self).__init__()
        self.resnet152 = torchvision.models.resnet152(pretrained=False)
        self.fc3 = nn.Linear(1000, 1)

    def forward(self, x):
        x = self.resnet152(x)
        x = self.fc3(x)
        return x


