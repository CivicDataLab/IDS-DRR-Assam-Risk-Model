import glob
import os

import rasterio
from rasterio.crs import CRS

# Specify the state information to scrape data for.
state_info = {"state": "Himachal Pradesh", "code": "hp"}

path = os.getcwd() + f"/Sources/BHUVAN/{state_info['state']}"
print("Base path: ", path)
files = glob.glob(path + "/data/tiffs/*.tif")
print("Files with watermark: ", files)

wm_removed_files = glob.glob(path + "/data/tiffs/removed_watermarks/*.tif")
print(wm_removed_files)

dates_watermark_removed = []


for file in wm_removed_files:
    dates_watermark_removed.append(file.split(r"/")[-1].split("_w")[0])

for file in files:
    date_string = file.split(r"/")[-1][:-4]
    if date_string in dates_watermark_removed:
        continue
    print(date_string)

    raster = rasterio.open(file)
    image1_ar = raster.read()

    # If Band4 is 255 it is definitely a inundated pixel based on observation
    image1_ar[3, :, :][(image1_ar[3, :, :] < 255.0)] = 0
    image1_ar[3, :, :][(image1_ar[3, :, :] == 255.0)] = 1

    meta = raster.meta
    meta["compress"] = "deflate"
    meta["count"] = 1  # Only one band.
    meta["dtype"] = "uint8"
    meta["crs"] = CRS.from_epsg(4326)
    meta["transform"] = raster.transform

    # Save the modified raster data to a new TIF file.
    # Band 4 is enough to identify inundation.
    with rasterio.open(
        path
        + "/data/tiffs/removed_watermarks/{}_watermarkremoved.tif".format(date_string),
        "w",
        **meta,
    ) as dst:
        dst.write(image1_ar[3, :, :], 1)
