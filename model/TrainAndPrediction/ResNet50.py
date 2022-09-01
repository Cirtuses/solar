from torch import nn
import torchvision


# Model architecture of resnet50
class ResNet50(nn.Module):
    def __init__(self):
        super(ResNet50, self).__init__()
        self.resnet50 = torchvision.models.resnet50(pretrained=True)
        self.fc3 = nn.Linear(1000, 1)

    def forward(self, x):
        x = self.resnet50(x)
        x = self.fc3(x)
        return x
