# -*- coding: utf-8 -*-
import os
from skimage import io


img_dir = r'J:\RockGlacier2\Segmentations\PNG'
save_dir = r'J:\RockGlacier2\Segmentations\PNGB'
img_names = os.listdir(img_dir)
for img_name in img_names:
    img_path = os.path.join(img_dir, img_name)
    img_ds = io.imread(img_path)
    dst_ds = img_ds[:, :, 0]
    dst_ds[dst_ds != 1] = 0
    dst_path = os.path.join(save_dir, img_name.rsplit('.', 1)[0] + '.png')
    io.imsave(dst_path, dst_ds)
