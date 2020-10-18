# -*- coding: utf-8 -*-
import os


idx_path = r'G:\ResearchArea\Nepal\iterrate.txt'
px_geosize = [1.9866146726862781, 1.9843750309028716]
pad_size = [150, 150]
pad_geosize = [a * b for a, b in zip(pad_size, px_geosize)]

mc = iface.mapCanvas()
layer = iface.activeLayer()
count = layer.featureCount()

if not os.path.exists(idx_path):
    with open(idx_path, 'w') as f:
        f.write(str(count))

with open(idx_path, 'r') as f:
    idx = int(f.readline())

if not idx - 1 < 0:
    idx -= 1
else:
    idx = 0

print(idx)
layer.selectByIds([idx])
bbox = layer.boundingBoxOfSelected()
extent = QgsRectangle(bbox.xMinimum() - pad_geosize[1], bbox.yMinimum() - pad_geosize[0],
                      bbox.xMaximum() + pad_geosize[1], bbox.yMaximum() + pad_geosize[0])
mc.setExtent(extent)
mc.refresh()
layer.selectByIds([])
with open(idx_path, 'w') as f:
    f.write(str(idx))