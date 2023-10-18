import rasterstats
import rasterio
import geopandas as gpd
import pandas as pd
import os
import glob
import numpy as np
import sys
path = os.getcwd()+'/Sources/WORLDPOP/'

year = sys.argv[1]
assam_rc_gdf = gpd.read_file(os.getcwd()+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')

# TOTAL POPULATION IN EACH RC
worldpop_raster = rasterio.open(path+'/data/population_counts/assam_ppp_{}_UNadj.tif'.format(year))
worldpop_raster_array = worldpop_raster.read(1)

sum_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(worldpop_raster.crs),
                                     worldpop_raster_array,
                                     affine= worldpop_raster.transform,
                                     stats= ['sum'],
                                     nodata=worldpop_raster.nodata,
                                     geojson_out = True)

dfs = []
for rc in sum_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

pop_zonal_stats_df = pd.concat(dfs).reset_index(drop=True)
pop_zonal_stats_df = pop_zonal_stats_df.rename(columns={'sum':'sum_population'})

# AVERAGE SEX RATIO IN EACH RC
sexratio_raster = rasterio.open(path+'/data/agesexstructure/sexratio_assam_{}.tif'.format(year))
sexratio_raster_array = sexratio_raster.read(1)

mean_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(sexratio_raster.crs),
                                     sexratio_raster_array,
                                     affine= sexratio_raster.transform,
                                     stats= ['mean'],
                                     nodata=sexratio_raster.nodata,
                                     geojson_out = True)

dfs = []
for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

sexratio_df = pd.concat(dfs).reset_index(drop=True)
sexratio_df = sexratio_df.rename(columns={'mean':'mean_sexratio'})
sexratio_df = sexratio_df[['object_id', 'mean_sexratio']]

# AGED POPULATION IN EACH RC
aged_raster = rasterio.open(path+'/data/agesexstructure/aged_population_assam_{}.tif'.format(year))
aged_raster_array = aged_raster.read(1)

sum_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(aged_raster.crs),
                                     aged_raster_array,
                                     affine= aged_raster.transform,
                                     stats= ['sum'],
                                     nodata=aged_raster.nodata,
                                     geojson_out = True)

dfs = []
for rc in sum_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

aged_pop_zonal_stats_df = pd.concat(dfs).reset_index(drop=True)
aged_pop_zonal_stats_df = aged_pop_zonal_stats_df.rename(columns={'sum':'sum_aged_population'})
aged_pop_zonal_stats_df = aged_pop_zonal_stats_df[['object_id', 'sum_aged_population']]

# YOUNG POPULATION IN EACH RC
young_raster = rasterio.open(path+'/data/agesexstructure/young_population_assam_{}.tif'.format(year))
young_raster_array = young_raster.read(1)

sum_dicts = rasterstats.zonal_stats(assam_rc_gdf.to_crs(young_raster.crs),
                                     young_raster_array,
                                     affine= young_raster.transform,
                                     stats= ['sum'],
                                     nodata=young_raster.nodata,
                                     geojson_out = True)

dfs = []
for rc in sum_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

young_pop_zonal_stats_df = pd.concat(dfs).reset_index(drop=True)
young_pop_zonal_stats_df = young_pop_zonal_stats_df.rename(columns={'sum':'sum_young_population'})
young_pop_zonal_stats_df = young_pop_zonal_stats_df[['object_id', 'sum_young_population']]

# MERGE ALL
merged_df = pop_zonal_stats_df.merge(sexratio_df, on='object_id')
merged_df = merged_df.merge(aged_pop_zonal_stats_df, on='object_id')
merged_df = merged_df.merge(young_pop_zonal_stats_df, on='object_id')

merged_df.to_csv(path+"data/worldpopstats_{}.csv".format(year), index=False)



