#ARCHIVE
import rasterio
from rasterio.transform import Affine
import numpy as np
import os

dem_path = os.getcwd()+'/Sources/NASADEM/data/NASADEM_DEM.tif'

raster = rasterio.open(dem_path)
dem_array = raster.read(1)

print(raster.transform.e)
# Calculate slope using numpy gradient function
slope_x, slope_y = np.gradient(dem_array, raster.transform.a, raster.transform.e)
slope_radians = np.arctan(np.sqrt(slope_x**2 + slope_y**2))

# Convert slope to degrees
slope_degrees = np.degrees(slope_radians)

# Copy the source metadata and update data type
meta = raster.meta.copy()
meta.update(dtype=rasterio.float32, count=1)

# Write slope data to a new raster
with rasterio.open(os.getcwd()+'/Sources/NASADEM/data/NASADEM_SLOPE_30.tif', 'w', **meta) as dst:
    dst.write(slope_degrees.astype(rasterio.float32), 1)
