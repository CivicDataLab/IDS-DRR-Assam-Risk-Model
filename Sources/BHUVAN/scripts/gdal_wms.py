import os
import time

path = os.getcwd()+'/Sources/BHUVAN/'

date_strings = ['2023_29_06_18', '2023_27_06_18', '2023_26_06_18', '2023_26_06_06', '2023_25_06_18',
               '2023_23_06_18', '2023_22_06_18', '2023_21_06_18', '2023_20_06_18', '2023_19_06_18', '2023_18_06',
               '2023_17_06_18', '2023_16_06_18']

for date_string in ['2023_18_06_18']:
     print(date_string)
     gdal_code = '''gdal_translate -of WMS "WMS:https://bhuvan-gp1.nrsc.gov.in/bhuvan/wms?&LAYERS=flood%3Aas_{}&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&BBOX=89.6922970,23.990548,96.0205936,28.1690311" {}data/inundation.xml'''.format(date_string,path)
     os.system(gdal_code)
     time.sleep(3)
     os.system("gdalwarp -tr 0.0001716660336923202072 -0.0001716684356881450775 {}data/inundation.xml {}data/tiffs/{}.tif -co COMPRESS=DEFLATE -co TILED=YES".format(path, path, date_string))
     time.sleep(10)