import torchvision
import torchvision.transforms as transforms
import torchvision.transforms.functional as TF
from PIL import Image

import numpy as np
import random



class RandomErasingTransform:
    """Implement Random Erasing (Zhong et al 2017) or my variations"""


    def __init__(self,
                 shape="rectangle",
                 erase_regions=1,
                 erase_prob=0.5,
                 erase_area_min=0.02, erase_area_max=0.4,
                 erase_aspect_min=0.3, erase_aspect_max=10/3):
        """Init random erasing transform

        New params not in original paper:
        shape: "rectangle", "ellipse", "diamond" 
        erase_regions: int
        """
        self.erase_regions = erase_regions
        self.shape = shape
        self.erase_prob = erase_prob
        self.erase_area_min, self.erase_area_max = erase_area_min, erase_area_max
        self.erase_aspect_min, self.erase_aspect_max = erase_aspect_min, erase_aspect_max

    def __call__(self, img):
        if random.random() > self.erase_prob:
            return img

        img_w, img_h = img.size
        img_area = img_w * img_h
        if self.shape == "ellipse": img_area *= 4 / np.pi
        elif self.shape == "diamond": img_area *= 2

        erase_regions_left = self.erase_regions
        
        while erase_regions_left > 0:
            # bounding box computations from original paper
            erase_area = img_area * np.random.uniform(self.erase_area_min, self.erase_area_max) / self.erase_regions
            erase_aspect = np.random.uniform(self.erase_aspect_min, self.erase_aspect_max)
            e_h = int((erase_area * erase_aspect)**0.5)
            e_w = int((erase_area / erase_aspect)**0.5)
            e_x = random.randrange(0, img_w)
            e_y = random.randrange(0, img_h)
            

            if e_x + e_w <= img_w and e_y + e_h <= img_h:  # bounding box fits
                erase_regions_left -= 1

                # modify pixels as np array (img_w, img_h, 3)
                a = np.array(img)

                if self.shape == "rectangle":
                    # fill with random pixels
                    a[e_y:e_y+e_h, e_x:e_x+e_w, :] = np.random.randint(0, 256, size=(e_h,e_w,3), dtype=np.uint8)

                else:
                    cx, cy = e_x + (e_w)/2, e_y + (e_h)/2
                    sx, sy = e_w/2, e_h/2  # radius of bounding box

                    for y in range(e_y, e_y+e_h):
                        for x in range(e_x, e_x+e_w):
                            # ellipse and diamond are stretched L2 and L1 balls
                            if self.shape == "ellipse":
                                dx, dy = (x-cx)**2 / sx**2, (y-cy)**2 / sy**2
                            elif self.shape == "diamond":
                                dx, dy = abs((x-cx) / sx), abs((y-cy) / sy)
                            else:
                                raise NotImplementedError

                            if dx + dy <= 1:
                                a[y,x,:] = np.random.randint(0, 256, size=3, dtype=np.uint8)

                img = Image.fromarray(a)  # replace original img

        return img


if __name__ == "__main__":
    testset = torchvision.datasets.CIFAR10(root='./data', train=False)
    img = testset[1][0]

    RandomErasingTransform(erase_regions=3, erase_prob=1)(img)\
        .resize((256,256), resample=Image.NEAREST).show()