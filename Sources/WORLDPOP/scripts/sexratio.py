import os
import glob
import rasterio
import sys

year = str(sys.argv[1])

# FEMALE
files = glob.glob('assam_f_*_{}.tif'.format(year))

raster = rasterio.open(files[0])
f_raster_array = raster.read(1)

for file in files[1:]:
   f_raster_array = f_raster_array + rasterio.open(file).read(1)

# SAVE THE TOTAL RASTER FOR THE YEAR
meta = raster.meta
meta['compress'] = 'deflate'
meta['crs'] = raster.crs
meta['transform'] = raster.transform

#with rasterio.open('annual_assam_f_{}.tif'.format(year), 'w', **meta) as dst:
 #   dst.write(f_raster_array, 1)


#MALE
files = glob.glob('assam_m_*_{}.tif'.format(year))

raster = rasterio.open(files[0])
m_raster_array = raster.read(1)

for file in files[1:]:
	m_raster_array = m_raster_array + rasterio.open(file).read(1)


sex_ratio_array = f_raster_array/m_raster_array

# SAVE THE SEX RATIO RASTER FOR THE YEAR

meta = raster.meta
meta['compress'] = 'deflate'
meta['crs'] = raster.crs
meta['transform'] = raster.transform

with rasterio.open('sexratio_assam_{}.tif'.format(year), 'w', **meta) as dst:
	dst.write(sex_ratio_array, 1)
