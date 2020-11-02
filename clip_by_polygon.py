# -*- coding: utf-8 -*-
import os
from osgeo import ogr


data_name = 'Himalaya'
shp_dir = r'G:\RockGlacier\Himalaya\Boundary\Himalaya.shp'
img_dir = r'G:\RockGlacier\Himalaya\QGIS\Bing'
wf_dir = r'G:\RockGlacier\Himalaya\QGIS\WorldFile'
img_suffix = 'jpg'
wf_suffix = 'jgw'

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

shp_ds = ogr.Open(shp_dir)
lyr = shp_ds.GetLayer()
geoms = ogr.Geometry(ogr.wkbMultiPolygon)
for feat in lyr:
    geom = feat.GetGeometryRef()
    if geom.GetGeometryName() == 'MULTIPOLYGON':
        for geom_part in geom:
            geoms.AddGeometry(geom_part)
    else:
        geoms.AddGeometry(geom)

# Polygon坐标范围[min_x, max_x, min_y, max_y]
lyr_extent = lyr.GetExtent()
# 以重叠尺寸略微扩大坐标范围，可删除
lyr_extent = [lyr_extent[0] - overlay_geosize[1], lyr_extent[1] + overlay_geosize[1],
             lyr_extent[2] - overlay_geosize[0], lyr_extent[3] + overlay_geosize[0]]

# 坐标范围内的按裁剪尺寸划分的条带数量
clip_count = [int((lyr_extent[3] - lyr_extent[2]) / offset_geosize[0]) + 1,
              int((lyr_extent[1] - lyr_extent[0]) / offset_geosize[1]) + 1]
print(clip_count)
max_len = len(str(max(clip_count)))

m, n = 0, 0
part_dir = os.path.join(img_dir, str(n))
if not os.path.exists(part_dir):
    os.mkdir(part_dir)
for i in range(clip_count[0]):
    for j in range(clip_count[1]):
        if m == 5000:
            m = 0
            n += 1
            part_dir = os.path.join(img_dir, str(n))
            if not os.path.exists(part_dir):
                os.mkdir(part_dir)

        # 待裁剪影像的坐标范围[min_x, min_y, max_x, max_y]
        clip_ext = (lyr_extent[0] + offset_geosize[0] * j,
                    lyr_extent[3] - offset_geosize[0] * i - clip_geosize[0],
                    lyr_extent[0] + offset_geosize[0] * j + clip_geosize[1],
                    lyr_extent[3] - offset_geosize[0] * i)

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
        img_name = data_name + '_{0}_{1}'.format(str(i).zfill(max_len), str(j).zfill(max_len))

        # 创建World File
        with open(os.path.join(wf_dir, img_name + '.' + wf_suffix), 'w') as f:
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
        image.save(os.path.join(part_dir, img_name + '.' + img_suffix))

        m += 1

print('task finished!')
