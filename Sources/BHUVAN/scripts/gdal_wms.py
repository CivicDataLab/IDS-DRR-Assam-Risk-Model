from PIL import Image
import os
import numpy as np
import rasterio

path = os.getcwd()+'/Sources/BHUVAN/'

#date_string = '2023_09_07_18'
#gdal_translate -of WMS "WMS:https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms?&LAYERS=flood%3Aas_"+date_string+"&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&BBOX=89.6922970,23.990548,96.0205936,28.1690311" inundation2.xml

#gdalwarp -tr 0.0001716660336923202072 -0.0001716684356881450775 inundation2.xml reservoirs.tif -co COMPRESS=DEFLATE -co TILED=YES


raster = rasterio.open(path+'data/tiffs/gdal_wms.tif')
image1_ar = raster.read()

# print(image1_ar.shape)
#print(image1_ar[0,:,:].max())
image1_ar[3,:,:][(image1_ar[3,:,:]<255.0)] = 0
image1_ar[3,:,:][(image1_ar[3,:,:]==255.0)] = 1

meta = raster.meta
meta['compress'] = 'deflate'
meta['count'] = 1 #Only one band.
meta['dtype'] = 'uint8'
meta['crs'] = raster.crs
meta['transform'] = raster.transform

# # Save the modified raster data to a new TIF file
with rasterio.open(path+'data/tiffs/gdal_wms_watermarkremoved.tif', 'w', **meta) as dst:
     dst.write(image1_ar[3,:,:], 1)