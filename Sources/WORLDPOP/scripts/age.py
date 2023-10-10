import os
import glob
import sys
import rasterio

year = str(sys.argv[1])
files = glob.glob('assam_*_*_{}.tif'.format(year))

above_65_files = []
young_files = []
for file in files:
	age = int(file.split('_')[2])
	if age >= 65:
		above_65_files.append(file)
	elif age <= 5:
		young_files.append(file)
	else:
		continue

raster = rasterio.open(above_65_files[0])
senior_raster_array = raster.read(1)

for file in above_65_files[1:]:
   senior_raster_array = senior_raster_array + rasterio.open(file).read(1)

# SAVE THE SENIOR CITIZENS RASTER FOR THE YEAR
meta = raster.meta
meta['compress'] = 'deflate'
meta['crs'] = raster.crs
meta['transform'] = raster.transform

with rasterio.open('aged_population_assam_{}.tif'.format(year), 'w', **meta) as dst:
    dst.write(senior_raster_array, 1)


# YOUNG RASTER
raster = rasterio.open(young_files[0])
young_raster_array = raster.read(1)

for file in young_files[1:]:
   young_raster_array = young_raster_array + rasterio.open(file).read(1)

# SAVE THE TOTAL RASTER FOR THE YEAR
meta = raster.meta
meta['compress'] = 'deflate'
meta['crs'] = raster.crs
meta['transform'] = raster.transform

with rasterio.open('young_population_assam_{}.tif'.format(year), 'w', **meta) as dst:
	dst.write(young_raster_array, 1)
