import torch
from config import parsers
from ResNet152 import ResNet152
from ResNet50 import ResNet50
from torchvision import transforms
from PIL import Image
import time


def load_model(model_path, model_name, device):
    if model_name == "ResNet50":
        net = ResNet50()
    elif model_name == "ResNet152":
        net = ResNet152()

    net = net.to(device)
    net.load_state_dict(torch.load(model_path, map_location='cpu'))
    # net = net.to(device)
    net.eval()
    return net


if __name__ == "__main__":
    opt = parsers()

    predict_normalize = transforms.Normalize(
        mean=[0.4922, 0.5424, 0.5440],
        std=[0.2952, 0.3117, 0.3254]
    )
    predict_trans = transforms.Compose([
        transforms.CenterCrop(480),
        transforms.ToTensor(),
        predict_normalize
    ])

    img_path = opt.predict_img
    target_type = opt.data_type
    data = predict_trans(Image.open(img_path))
    model_path = opt.load_model
    model_name = opt.model_name

    # img_path = r'D:/PythonWorks/solar_project/5min-300s-regular/DNI/LR/test/' \
    #            r'3408-2021-04-25 09-05-00-561-342-298-.jpg'
    # target_type = 'ghi'
    # net = ResNet152()
    # net.eval()
    # data = predict_trans(Image.open(img_path))
    # data = data.unsqueeze(0)
    # a = net(data)
    # result = a.item()

    data = data.unsqueeze(0)
    device = torch.device("cpu")
    net = load_model(model_path=model_path, model_name=model_name, device=device)
    start_test = time.time()
    result = net(data)
    result = result.item()

    if target_type == 'ghi':
        result = result * 1000.0
        print("this image's ghi is " + str(round(result, 2)))
    elif target_type == 'dhi':
        result = result * 600.0
        print("this image's dhi is " + str(round(result, 2)))
    else:
        result = result * 800.0
        print("this image's dni is " + str(round(result, 2)))
        
    end_test = time.time()
    print("cost time is: " + str(end_test - start_test))





