import rasterstats
import rasterio
import geopandas as gpd
import pandas as pd
import os
import glob
import numpy as np
import time

tic = time.perf_counter()
month= '06'
year ='2023'
path = os.getcwd()+'/Sources/BHUVAN/'
assam_rc_gdf = gpd.read_file(os.getcwd()+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')

files = glob.glob(path+"data/tiffs/removed_watermarks/"+year+"_*_"+month+"*.tif")
print('Number of maps available for the month: ',len(files))

raster = rasterio.open(files[0])
raster_array = raster.read(1)

for file in files[1:]:
    raster_array = raster_array + rasterio.open(file).read(1)

# SAVE THE STITCHED RASTER FOR THE MONTH
meta = raster.meta
meta['compress'] = 'deflate'
meta['count'] = 1 #Only one band.
meta['dtype'] = 'int8'
meta['crs'] = raster.crs
meta['transform'] = raster.transform
meta['nodata'] = -1

with rasterio.open(path+'data/tiffs/stitched_monthly/stitched_{}_{}.tif'.format(year,month), 'w', **meta) as dst:
    dst.write(raster_array, 1)

# CALCULATE MODEL INPUTS
def count_nonzero(x):
    return np.count_nonzero(x)


mean_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(raster.crs),
                                     raster_array,
                                     affine= raster.transform,
                                     stats= ['count'],
                                     nodata=raster.nodata,
                                     add_stats={'count_nonzero':count_nonzero},
                                     geojson_out = True)

dfs = []
for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

zonal_stats_df = pd.concat(dfs).reset_index(drop=True)
zonal_stats_df['inundation_pct'] = zonal_stats_df['count_nonzero']/zonal_stats_df['count']

# INTENSITY
intensity_array = np.divide(raster_array, raster_array.max())
def nonzero_mean(x):
    nonzero_values = x[x != 0]
    return np.mean(nonzero_values)

mean_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(raster.crs),
                                     intensity_array,
                                     affine= raster.transform,
                                     stats= ['mean', 'sum'],
                                              nodata=raster.nodata,
                                              add_stats={'intensity_mean_nonzero':nonzero_mean},
                                              geojson_out = True)

dfs = []
for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

intensity_df = pd.concat(dfs).reset_index(drop=True)

intensity_df.rename(columns = {'mean':'intensity_mean', 'sum':'intensity_sum'}, inplace = True)

zonal_stats_df = pd.merge(zonal_stats_df, intensity_df[['intensity_mean','intensity_mean_nonzero','intensity_sum','object_id']], on='object_id')

zonal_stats_df.to_csv(path+"data/inundation_pct/inundation_pct"+year+"_"+month+".csv")

toc = time.perf_counter()
print("Time Taken: {} seconds".format(toc-tic))