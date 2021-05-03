import torch
import torchvision
import torchvision.transforms as transforms


testset = torchvision.datasets.CIFAR10(root='./data', train=False)

img = testset[0][0]

random_crop = transforms.RandomCrop(32, padding=4)

random_crop.forward(img).resize((256, 256)).show()