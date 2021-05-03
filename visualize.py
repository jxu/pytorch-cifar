import torchvision
import torchvision.transforms as transforms
import torchvision.transforms.functional as TF
from PIL import Image

import numpy as np
import random

class RandomErasingTransform:
    """Implement Random Erasing (Zhong et al 2017) or my variations"""

    def __init__(self,
                 erase_prob=0.5,
                 erase_area_min=0.02, erase_area_max=0.4,
                 erase_aspect_min=0.3, erase_aspect_max=10/3):
        self.erase_prob = erase_prob
        self.erase_area_min, self.erase_area_max = erase_area_min, erase_area_max
        self.erase_aspect_min, self.erase_aspect_max = erase_aspect_min, erase_aspect_max

    def __call__(self, img):
        if random.random() > self.erase_prob:
            return img

        img_w, img_h = img.size
        img_area = img_w * img_h
        
        while True:
            erase_area = img_area * np.random.uniform(self.erase_area_min, self.erase_area_max)
            erase_aspect = np.random.uniform(self.erase_aspect_min, self.erase_aspect_max)
            e_h = int((erase_area * erase_aspect)**0.5)
            e_w = int((erase_area / erase_aspect)**0.5)
            e_x = random.randrange(0, img_w)
            e_y = random.randrange(0, img_h)
            if e_x + e_w <= img_w and e_y + e_h <= img_h:
                # modify pixels as np array (img_w, img_h, 3)
                a = np.array(img)
                a[e_y:e_y+e_h, e_x:e_x+e_w, :] = np.random.randint(0, 256, size=(e_h,e_w,3), dtype=np.uint8)
                return Image.fromarray(a)



testset = torchvision.datasets.CIFAR10(root='./data', train=False)
img = testset[1][0]

RandomErasingTransform()(img).resize((256,256), resample=Image.NEAREST).show()