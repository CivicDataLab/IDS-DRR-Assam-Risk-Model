import glob
import os
import sys
import time

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import rasterstats

if len(sys.argv) < 3:
    print("Please provide an input argument.")
else:
    print(sys.argv)
    year = str(sys.argv[1])
    month = str(sys.argv[2])
    print("Month: ", year + month)

tic = time.perf_counter()
path = os.getcwd() + "/Sources/BHUVAN/assam/"
assam_rc_gdf = gpd.read_file(
    os.getcwd() + "/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp"
)

files1 = glob.glob(
    path + "data/tiffs/removed_watermarks/" + year + "_??_" + month + "*.tif"
)
files2 = glob.glob(
    path + "data/tiffs/removed_watermarks/" + year + "_??-??_" + month + "*.tif"
)
files = files1 + files2
print("Number of maps available for the month: ", len(files))

raster = rasterio.open(files[0])
raster_array = raster.read(1)


for file in files[1:]:
    raster_array = raster_array + rasterio.open(file).read(1)

# SAVE THE STITCHED RASTER FOR THE MONTH
meta = raster.meta
meta["compress"] = "deflate"
meta["count"] = 1  # Only one band.
meta["dtype"] = "int8"
meta["crs"] = raster.crs
meta["transform"] = raster.transform
meta["nodata"] = -1

with rasterio.open(
    path + "data/tiffs/stitched_monthly/stitched_{}_{}.tif".format(year, month),
    "w",
    **meta
) as dst:
    dst.write(raster_array, 1)


# CALCULATE MODEL INPUTS
def count_nonzero(x):
    return np.count_nonzero(x.compressed())


mean_dicts = rasterstats.zonal_stats(
    assam_rc_gdf.to_crs(raster.crs),
    raster_array,
    affine=raster.transform,
    stats=["count"],
    nodata=raster.nodata,
    add_stats={"count_nonzero": count_nonzero},
    geojson_out=True,
)

# Convert the dictionary items to a list and slice to get the last 5 items
dfs = []
for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc["properties"]]))

zonal_stats_df = pd.concat(dfs).reset_index(drop=True)
zonal_stats_df["inundation_pct"] = (
    zonal_stats_df["count_nonzero"] / zonal_stats_df["count"]
)

# INTENSITY - maximum inundated pixel has INTENSITY 1
intensity_array = np.divide(raster_array, raster_array.max())


def nonzero_mean(x):
    x = x.compressed()
    nonzero_values = x[x != 0]
    return np.mean(nonzero_values)


mean_dicts = rasterstats.zonal_stats(
    assam_rc_gdf.to_crs(raster.crs),
    intensity_array,
    affine=raster.transform,
    stats=["mean", "sum"],
    nodata=raster.nodata,
    add_stats={"intensity_mean_nonzero": nonzero_mean},
    geojson_out=True,
)

dfs = []
for rc in mean_dicts:
    dfs.append(pd.DataFrame([rc["properties"]]))

intensity_df = pd.concat(dfs).reset_index(drop=True)

intensity_df.rename(
    columns={"mean": "intensity_mean", "sum": "intensity_sum"}, inplace=True
)

zonal_stats_df = pd.merge(
    zonal_stats_df,
    intensity_df[
        ["intensity_mean", "intensity_mean_nonzero", "intensity_sum", "object_id"]
    ],
    on="object_id",
)

zonal_stats_df = zonal_stats_df[
    [
        "object_id",
        "count",
        "count_nonzero",
        "inundation_pct",
        "intensity_mean",
        "intensity_mean_nonzero",
        "intensity_sum",
    ]
]

zonal_stats_df.columns = [
    "object_id",
    "count_bhuvan_pixels",
    "count_inundated_pixels",
    "inundation_pct",
    "inundation_intensity_mean",
    "inundation_intensity_mean_nonzero",
    "inundation_intensity_sum",
]

if os.path.exists(path + "data/variables/inundation_pct"):
    zonal_stats_df.to_csv(
        path
        + "/data/variables/inundation_pct/"
        + "inundation_pct_"
        + year
        + "_"
        + month
        + ".csv",
        index=False,
    )
else:
    os.mkdir(path + "data/variables/inundation_pct")
    zonal_stats_df.to_csv(
        path
        + "/data/variables/inundation_pct/"
        + "inundation_pct_"
        + year
        + "_"
        + month
        + ".csv",
        index=False,
    )

toc = time.perf_counter()
print("Time Taken: {} seconds".format(toc - tic))
