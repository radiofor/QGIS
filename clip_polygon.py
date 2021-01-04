# -*- coding: utf-8 -*-
import os
from osgeo import ogr


data_name = 'Nepal'
shp_dir = r'J:\RockGlacier2\Nepal200.shp'
img_dir = r'J:\RockGlacier2\Segmentations\PNG'
wf_dir = r'J:\RockGlacier2\WorlfFiles'
img_suffix = 'jpg'
wf_suffix = 'jgw'

# 像素[高, 宽]
px_geosize = [2.645859085290482, 2.6458015267176016]
# 单幅影像的像素尺寸
clip_size = [1000, 1000]
# 单幅影像的坐标尺寸
clip_geosize = [a * b / 2 for a, b in zip(clip_size, px_geosize)]

shp_ds = ogr.Open(shp_dir)
lyr = shp_ds.GetLayer()
count = lyr.GetFeatureCount()
i = 0
for feat in lyr:
    geom = feat.GetGeometryRef()
    extent = geom.GetEnvelope()

    # ctr_x, ctr_y
    centre = [(extent[1] + extent[0]) / 2, (extent[3] + extent[2]) / 2]

    clip_ext = [centre[0] - clip_geosize[1], centre[1] - clip_geosize[0],
                centre[0] + clip_geosize[1], centre[1] + clip_geosize[0]]

    # 设置名称
    img_name = data_name + '_{0}'.format(i)
    i += 1

    # 创建World File
    # with open(os.path.join(wf_dir, img_name + '.' + wf_suffix), 'w') as f:
    #     f.writelines([str(px_geosize[0]) + '\n', str(0) + '\n', str(0) + '\n',
    #                   str(-px_geosize[1]) + '\n', str(clip_ext[0]) + '\n', str(clip_ext[3]) + '\n'])

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
    image.save(os.path.join(img_dir, img_name + '.' + img_suffix))

print('task finished!')
