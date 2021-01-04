# -*- coding: utf-8 -*-


# 坐标范围[西, 南, 东, 北]
extent = [9307848.3435, 3367361.7993, 9311059.0622, 3369121.9400]
# 输出像素尺寸[高, 宽]
output_size = [887, 1618]

px_geosize = [(extent[3] - extent[1]) / output_size[0], (extent[2] - extent[0]) / output_size[1]]
print('Geosize of Pixel:', px_geosize)
