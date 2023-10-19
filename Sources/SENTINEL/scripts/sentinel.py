import ee
import geemap
import os 
import time
import rasterio
import geopandas as gpd
import rasterstats
import pandas as pd
import sys

service_account = ' idsdrr@ee-idsdrr.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'Sources/SENTINEL/ee-idsdrr-d856f70748a7.json')
ee.Initialize(credentials)

if len(sys.argv) < 3:
    print("Please provide an input argument.")
else:
    date_start = sys.argv[1]
    date_end = sys.argv[2]
    print("Date End:", date_end)

cwd = os.getcwd()
assam_rc_gdf = gpd.read_file(cwd+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')
assam_dist_gdf = gpd.read_file(cwd+'/Maps/assam_district_35.geojson')

#Function for Zonal Stats
def zonal_stats_choropleths(gdf,
                            gdf_unique_id,
                            raster,
                            stats_list=['mean', 'count'],
                            ):
    mean_dicts = rasterstats.zonal_stats(gdf.to_crs(raster.crs),
                                              raster.read(1),
                                              affine= raster.transform,
                                              stats= stats_list,
                                              nodata=raster.nodata,
                                              geojson_out = True)
    dfs = []
    for rc in mean_dicts:
        dfs.append(pd.DataFrame([rc['properties']]))
        
    zonal_stats_df = pd.concat(dfs).reset_index(drop=True)
    
    zonal_stats_gdf = pd.merge(gdf,
                               zonal_stats_df[stats_list+[gdf_unique_id]],
                               on=gdf_unique_id)
    
    zonal_stats_gdf = gpd.GeoDataFrame(zonal_stats_gdf)

    return zonal_stats_df, zonal_stats_gdf


# clip_image function clips the satellite image to our given area of interest
def clip_image(aoi):
    def call_image(image):
        return image.clip(aoi)
    return call_image

# Function to mask clouds
def maskS2clouds(image):
    qa = image.select('QA60')

    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudBitMask).eq(0)
    mask = mask.bitwiseAnd(cirrusBitMask).eq(0)

    return image.updateMask(mask).divide(10000)

assam_rcs = ee.FeatureCollection("projects/ee-idsdrr/assets/assam_rc_180")
geometry = assam_rcs.geometry() 

# Get GEE Image Collection
sentinel = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")

# Filter the image collection
sentinel_filtered = sentinel \
                    .filter(ee.Filter.date(date_start, date_end)) \
                    .filter(ee.Filter.bounds(geometry)) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) # Filter for images that have less then 20% cloud coverage.

# Apply cloud mask
sentinel_filtered_cloud_masked = sentinel_filtered.map(maskS2clouds)

# Choose median image
sentinel_median = sentinel_filtered_cloud_masked.median()

ndvi = sentinel_median.normalizedDifference(['B8', 'B4']).rename('ndvi')
ndbi = sentinel_median.normalizedDifference(['B11', 'B8']).rename('ndbi')




print("-------NDVI Image-------------")

path=cwd+'/Sources/SENTINEL/data/NDVI/tifs/'
geemap.ee_export_image(ndvi,
                       filename=path+'ndvi_{}.tif'.format(date_end),
                       scale=250,
                       region=geometry,
                       file_per_band=True)

print("-------NDBI Image-------------")
path=cwd+'/Sources/SENTINEL/data/NDBI/tifs/'
geemap.ee_export_image(ndbi,
                       filename=path+'ndbi_{}.tif'.format(date_end),
                       scale=250,
                       region=geometry,
                       file_per_band=True)

print("-------NDVI Stats-------------")
# # geemap.zonal_statistics(ndvi,
# #                         assam_rcs,
# #                         cwd+'/Sources/SENTINEL/data/ndvi_{}.csv'.format(date_end),
# #                         statistics_type='MEAN',
# #                         scale=1000)
ndvi_raster = rasterio.open(cwd+'/Sources/SENTINEL/data/NDVI/tifs/ndvi_{}.ndvi.tif'.format(date_end))

ndvi_rc_df, ndvi_rc_gdf = zonal_stats_choropleths(assam_rc_gdf,'object_id',
                                                  ndvi_raster)

#ndvi_dist_df, ndvi_dist_gdf = zonal_stats_choropleths(assam_dist_gdf, 'assam_dist',
 #                                                 ndvi_raster)

ndvi_rc_df = ndvi_rc_df[['object_id', 'mean']]
ndvi_rc_df = ndvi_rc_df.replace(columns = {'mean': 'mean_ndvi'})
ndvi_rc_df.to_csv(cwd+'/Sources/SENTINEL/data/NDVI/csvs/mean_ndvi_{}.csv'.format(date_end),
                index=False)
ndvi_rc_gdf.to_file(cwd+'/Sources/SENTINEL/data/NDVI/geojsons/ndvi_rc_{}.geojson'.format(date_end))


#ndvi_dist_df.to_csv(cwd+'/Sources/SENTINEL/data/NDVI/csvs/ndvi_dist_{}.csv'.format(date_end),
               # index=False)
#ndvi_dist_gdf.to_file(cwd+'/Sources/SENTINEL/data/NDVI/geojsons/ndvi_dist_{}.geojson'.format(date_end))


print("-------NDBI Stats-------------")
# geemap.zonal_statistics(ndbi,
#                         assam_rcs,
#                         cwd+'/Sources/SENTINEL/data/ndbi_{}.csv'.format(date_end),
#                         statistics_type='MEAN',
#                         scale=1000)

ndbi_raster = rasterio.open(cwd+'/Sources/SENTINEL/data/NDBI/tifs/ndbi_{}.ndbi.tif'.format(date_end))
ndbi_rc_df, ndbi_rc_gdf = zonal_stats_choropleths(assam_rc_gdf,'object_id',
                                                  ndbi_raster)

#ndbi_dist_df, ndbi_dist_gdf = zonal_stats_choropleths(assam_dist_gdf, 'assam_dist',
 #                                                 ndbi_raster)

ndbi_rc_df = ndbi_rc_df[['object_id', 'mean']]
ndbi_rc_df = ndbi_rc_df.replace(columns = {'mean': 'mean_ndbi'})
ndbi_rc_df.to_csv(cwd+'/Sources/SENTINEL/data/NDBI/csvs/ndbi_rc_{}.csv'.format(date_end),
                index=False)
ndbi_rc_gdf.to_file(cwd+'/Sources/SENTINEL/data/NDBI/geojsons/mean_ndbi_{}.geojson'.format(date_end))


#ndbi_dist_df.to_csv(cwd+'/Sources/SENTINEL/data/NDBI/csvs/ndbi_dist_{}.csv'.format(date_end),
 #               index=False)
#ndbi_dist_gdf.to_file(cwd+'/Sources/SENTINEL/data/NDBI/geojsons/ndbi_dist_{}.geojson'.format(date_end))
