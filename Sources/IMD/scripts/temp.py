import os
import calendar
import rasterio
import rasterstats
import pandas as pd
import imdlib as imd
import geopandas as gpd
import numpy as np
from rasterio.crs import CRS
from rasterio.windows import Window

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.abspath(CURRENT_FOLDER + '/../' + 'data')

TIFF_DATA_FOLDER = os.path.join(DATA_FOLDER, 'rain', 'tiff')

ASSAM_REVENUE_CIRCLE_GDF = gpd.read_file(
    os.getcwd() + '/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp'
)

with rasterio.open(TIFF_DATA_FOLDER + '/2018-Aug.tif', 'r+') as raster:
    raster.crs = CRS.from_epsg(4326)
    raster_array = raster.read(1, window=Window(0,0,129,135))

    nan_mask = np.isnan(raster_array)
    raster_array[nan_mask] = -999

    raster.nodata = -999

# print(raster_array)

# print(raster.transform)
# exit()

mean_dicts = rasterstats.zonal_stats(
    ASSAM_REVENUE_CIRCLE_GDF.to_crs(raster.crs),
    raster_array.squeeze(),
    affine=raster.transform,
    stats= ['mean', 'count'],
    nodata=raster.nodata
    # geojson_out = True
)

dfs = []

for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc['properties']]))

zonal_stats_df = pd.concat(dfs).reset_index(drop=True)

print(zonal_stats_df)