# -*- coding: utf-8 -*-
import os
from PIL import Image
import numpy as np


img_dir = r'G:\RockGlacier\Himalaya\QGIS\Lable\0'
wf_dir = r'G:\RockGlacier\Himalaya\QGIS\WorldFile\0'
idx_path = r'G:\RockGlacier\Himalaya\VOC\Index\val.txt'
img_suffix = 'jpg'
wf_suffix = 'jgw'

# 单幅影像的像素尺寸
clip_size = [1000, 1000]

wf_names = []
if os.path.exists(idx_path):
    with open(idx_path, 'r') as f:
        line = f.readline().strip()
        while line:
            wf_name = line + '.' + wf_suffix
            wf_names.append(wf_name)
            line = f.readline().strip()
else:
    wf_names = os.listdir(wf_dir)

for wf_name in wf_names:
    wf_path = os.path.join(wf_dir, wf_name)
    wf_paras = []
    with open(wf_path, 'r') as f:
        wf_para = f.readline()
        while wf_para:
            wf_paras.append(float(wf_para))
            wf_para = f.readline()

    # 待裁剪影像的坐标范围[min_x, min_y, max_x, max_y]
    clip_ext = (wf_paras[4],
                wf_paras[5] + wf_paras[3] * clip_size[1],
                wf_paras[4] + wf_paras[0] * clip_size[0],
                wf_paras[5])

    # 设置名称
    img_name = os.path.splitext(wf_name)[0]

    # 将待裁剪影像的坐标范围转为QGIS格式
    rect = QgsRectangle(clip_ext[0], clip_ext[1], clip_ext[2], clip_ext[3])

    # 图片保存设置
    settings = iface.mapCanvas().mapSettings()
    # 设置图片分辨率，默认为96 dpi，若不改可以不写
    settings.setOutputDpi(96)
    # 设置坐标范围
    settings.setExtent(rect)
    # 设置像素尺寸
    settings.setOutputSize(QSize(clip_size[1], clip_size[0]))
    job = QgsMapRendererSequentialJob(settings)
    job.start()
    job.waitForFinished()
    image = job.renderedImage()
    img_path = os.path.join(img_dir, img_name + '.' + img_suffix)
    image.save(img_path)
print('task finished!')