# -*- coding: utf-8 -*-
import os
from osgeo import ogr


data_name = ''
shp_path = r'G:\RockGlacier\India\Himachal\Boundary\Himachal.shp'
img_path = r'G:\RockGlacier\India\Himachal\QGIS\Google'
wf_path = r'G:\RockGlacier\India\Himachal\QGIS\WorldFile'
img_suffix = 'jpg'
wf_suffix = 'jpw'

# 像素[高, 宽]
px_geosize = [2.645859085290482, 2.6458015267176016]
# 单幅影像的像素尺寸
clip_size = [1000, 1000]
# 重叠区域的像素尺寸
overlay_size = [200, 200]
# 单幅影像的坐标尺寸
clip_geosize = [a * b for a, b in zip(clip_size, px_geosize)]
# 重叠区域的坐标尺寸
overlay_geosize = [a * b for a, b in zip(overlay_size, px_geosize)]
# 每次裁剪偏移的坐标尺寸
offset_geosize = [a - b for a, b in zip(clip_geosize, overlay_geosize)]

shp_ds = ogr.Open(shp_path)
lyr = shp_ds.GetLayer()
geoms = ogr.Geometry(ogr.wkbMultiPolygon)
for feat in lyr:
    geoms.AddGeometry(feat.GetGeometryRef())

# Polygon坐标范围[min_x, max_x, min_y, max_y]
geom_evlp = geoms.GetEnvelope()
# 以重叠尺寸略微扩大坐标范围，可删除
geom_evlp = [geom_evlp[0] - overlay_geosize[1], geom_evlp[1] + overlay_geosize[1],
             geom_evlp[2] - overlay_geosize[0], geom_evlp[3] + overlay_geosize[0]]

# 坐标范围内的按裁剪尺寸划分的条带数量
clip_count = [int((geom_evlp[3] - geom_evlp[2]) / offset_geosize[0]) + 1,
              int((geom_evlp[1] - geom_evlp[0]) / offset_geosize[1]) + 1]
print(clip_count)

for i in range(clip_count[0]):
    for j in range(clip_count[1]):
        # 待裁剪影像的坐标范围[min_x, min_y, max_x, max_y]
        clip_ext = (geom_evlp[0] + offset_geosize[0] * j,
                    geom_evlp[3] - offset_geosize[0] * i - clip_geosize[0],
                    geom_evlp[0] + offset_geosize[0] * j + clip_geosize[1],
                    geom_evlp[3] - offset_geosize[0] * i)

        # 根据单幅影像的地理范围创建Polygon
        clip_ring = ogr.Geometry(ogr.wkbLinearRing)
        clip_ring.AddPoint(clip_ext[0], clip_ext[1])
        clip_ring.AddPoint(clip_ext[2], clip_ext[1])
        clip_ring.AddPoint(clip_ext[2], clip_ext[3])
        clip_ring.AddPoint(clip_ext[0], clip_ext[3])
        clip_ring.AddPoint(clip_ext[0], clip_ext[1])
        clip_geom = ogr.Geometry(ogr.wkbPolygon)
        clip_geom.AddGeometry(clip_ring)
        # 若该幅影像坐标范围不与任何Polygon相交，则跳过裁剪
        if not geoms.Intersect(clip_geom):
            continue

        # 设置名称
        name = data_name + '_{0}_{1}'.format(str(i).zfill(3), str(j).zfill(3))

        # 创建World File
        with open(os.path.join(wf_path, name + '.' + wf_suffix), 'w') as f:
            f.writelines([str(px_geosize[0]) + '\n', str(0) + '\n', str(0) + '\n',
                          str(-px_geosize[1]) + '\n', str(clip_ext[0]) + '\n', str(clip_ext[3]) + '\n'])

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
        image.save(os.path.join(img_path, name + '.' + img_suffix))

print('task finished!')
