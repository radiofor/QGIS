# -*- coding: utf-8 -*-
import os


idx_path = r'G:\RockGlacier\Himalaya\Boundary\iterrate.txt'
px_geosize = [2.645859085290482, 2.6458015267176016]
pad_size = [10, 10]
pad_geosize = [a * b for a, b in zip(pad_size, px_geosize)]

mc = iface.mapCanvas()
layer = iface.activeLayer()
count = layer.featureCount()

if not os.path.exists(idx_path):
    with open(idx_path, 'w') as f:
        f.write(str(-1))

with open(idx_path, 'r') as f:
    idx = int(f.readline())

if idx + 1 < count:
    idx += 1
else:
    idx = count - 1

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
