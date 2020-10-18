# -*- coding: utf-8 -*-


# 坐标范围[西, 南, 东, 北]
extent = [9500353.3498, 3336838.0024, 9503564.0686, 3338598.1430]
# 输出像素尺寸[高, 宽]
output_size = [886, 1618]

px_geosize = [(extent[3] - extent[1]) / output_size[0], (extent[2] - extent[0]) / output_size[1]]
print('Geosize of Pixel:', px_geosize)
