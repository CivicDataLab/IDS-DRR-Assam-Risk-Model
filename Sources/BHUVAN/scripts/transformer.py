import rasterstats
import rasterio
import geopandas as gpd
import pandas as pd
import os
import glob
import numpy as np

month= '06'
year ='2023'
path = os.getcwd()+'/Sources/BHUVAN/'
assam_rc_gdf = gpd.read_file(os.getcwd()+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')

files = glob.glob(path+"data/tiffs/"+year+"_*_"+month+"*.tif")

raster = rasterio.open(files[0])
raster_array = raster.read(1)

for file in files[1:]:
    raster_array = raster_array + rasterio.open(file).read(1)

print(raster_array.max())
mean_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(raster.crs),raster_array,
                                             affine= raster.transform,
                                              stats= ['mean', 'count'],
                                              #nodata=raster.nodata,
                                              geojson_out = True)

dfs = []
for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

zonal_stats_df = pd.concat(dfs).reset_index(drop=True)

zonal_stats_df.rename(columns = {'mean':'inundation_pct'}, inplace = True)

# INTENSITY
intensity_array = np.divide(raster_array, raster_array.max())
print(intensity_array.max())
mean_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(raster.crs),intensity_array,
                                             affine= raster.transform,
                                              stats= ['mean', 'sum'],
                                              #nodata=raster.nodata,
                                              geojson_out = True)

dfs = []
for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

intensity_df = pd.concat(dfs).reset_index(drop=True)

intensity_df.rename(columns = {'mean':'intensity_mean', 'sum':'intensity_sum'}, inplace = True)

zonal_stats_df = pd.merge(zonal_stats_df, intensity_df[['intensity_mean','intensity_sum','object_id']], on='object_id')

zonal_stats_df.to_csv(path+"data/inundation_pct/inundation_pct"+year+"_"+month+".csv")
