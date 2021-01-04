# -*- coding: utf-8 -*-
import os
from skimage import io
import numpy as np


img_path = r'J:\VOC\Labels\Himalaya_17_15.png'
img_ds = io.imread(img_path)
print('shape:', img_ds.shape)
print('unique:', np.unique(img_ds))
