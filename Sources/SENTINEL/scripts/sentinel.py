import ee
import geemap
import os 
import time

date_start = '2022-01-01'
date_end ='2022-02-01'

tic = time.perf_counter()
cwd = os.getcwd()

service_account = ' idsdrr@ee-idsdrr.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'Sources/SENTINEL/ee-idsdrr-d856f70748a7.json')
ee.Initialize(credentials)

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
sentinel_median = sentinel_filtered_cloud_masked.mosaic()

ndvi = sentinel_median.normalizedDifference(['B8', 'B4']).rename('ndvi')
ndbi = sentinel_median.normalizedDifference(['B11', 'B8']).rename('ndbi')

print("-------NDVI Image-------------")
geemap.ee_export_image(ndvi,
                       filename=cwd+'/Sources/SENTINEL/data/ndvi_{}.tif'.format(date_end),
                       scale=1000,
                       region=geometry,
                       file_per_band=True)
print("-------NDBI Image-------------")

geemap.ee_export_image(ndbi,
                       filename=cwd+'/Sources/SENTINEL/data/ndbi_{}.tif'.format(date_end),
                       scale=1000,
                       region=geometry,
                       file_per_band=True)
print("-------NDVI Stats-------------")

geemap.zonal_statistics(ndvi,
                        assam_rcs,
                        cwd+'/Sources/SENTINEL/data/ndvi_{}.csv'.format(date_end),
                        statistics_type='MEAN',
                        scale=1000)
print("-------NDBI Stats-------------")
geemap.zonal_statistics(ndbi,
                        assam_rcs,
                        cwd+'/Sources/SENTINEL/data/ndbi_{}.csv'.format(date_end),
                        statistics_type='MEAN',
                        scale=1000)
toc = time.perf_counter()
print("Time Taken: {} seconds".format(toc-tic))