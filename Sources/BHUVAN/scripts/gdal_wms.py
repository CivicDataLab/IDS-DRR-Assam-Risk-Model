
date_string = '2023_09_07_18'
gdal_translate -of WMS "WMS:https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms?&LAYERS=flood%3Aas_"+date_string+"&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&BBOX=89.6922970,23.990548,96.0205936,28.1690311" inundation2.xml

gdalwarp -tr 0.0001716660336923202072 -0.0001716684356881450775 inundation2.xml reservoirs.tif -co COMPRESS=DEFLATE -co TILED=YES