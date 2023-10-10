import rasterstats
import rasterio
import geopandas as gpd
import pandas as pd
import os
import glob
import numpy as np
path = os.getcwd()+'/Sources/WORLDPOP/'

assam_rc_gdf = gpd.read_file(os.getcwd()+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')

worldpop_raster = rasterio.open(path+'/data/assam_ppp_2020_UNadj.tif')
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

pop_zonal_stats_df.to_csv(path+"data/assam_ppp_2020_UNadj.csv", index=False)



