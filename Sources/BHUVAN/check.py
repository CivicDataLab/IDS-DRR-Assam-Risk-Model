import xarray as xr
import rioxarray

nc_path = '/home/krishna/IDS-DRR-Data-Pipeline/Sources/BHUVAN/NCs/2016_26_04_18.nc'

def create_tiffs_from_ncs(nc_path, image_name):
    '''
    Creates GeoTIFF files from the NetCDF4 files.

    Input parameters:
    nc_path: filepath of the NetCDF4 file.
    image_name: Output name of the GeoTIFF
    '''

    nc_file = xr.open_dataset(nc_path)
    var = nc_file['Inundation']

    var = var.rio.set_spatial_dims('lon', 'lat')
    var.rio.set_crs("epsg:4326")
    var.rio.to_raster(path+r"/tiffs/" + image_name + r".tif")
    nc_file.close()

create_tiffs_from_ncs(nc_path, "2016_26_04_18")