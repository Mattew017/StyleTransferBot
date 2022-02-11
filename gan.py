import os
import torch
import torchvision.transforms as transforms
from PIL import Image


class GAN:
    def __init__(self, _type):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if _type == "vangogh":
            self.model = torch.load(os.path.join("my_models", "vangogh.pth")).to(self.device)
        else:
            self.model = torch.load(os.path.join("my_models", "monet.pth")).to(self.device)

        for p in self.model.parameters():
            p.requires_grad = False

    def transfer(self, img_path, imsize=512):
        img = self.image_loader(img_path, imsize)
        result = self.model(img)
        result = result.add(1).div(2)  # [-1;1] -> [0;1]
        return result

    def image_loader(self, image_name, imsize):
        loader = transforms.Compose([
            transforms.Resize(imsize),
            transforms.CenterCrop(imsize),
            transforms.ToTensor()])

        image = Image.open(image_name)
        image = loader(image).unsqueeze(0)
        return image.to(self.device, torch.float)


if __name__ == '__main__':
    pass
