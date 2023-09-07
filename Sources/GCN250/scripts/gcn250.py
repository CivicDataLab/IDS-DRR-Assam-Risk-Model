import ee
import geemap
import os 
import time
import rasterio
import geopandas as gpd
import rasterstats
import pandas as pd

service_account = ' idsdrr@ee-idsdrr.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'Sources/SENTINEL/ee-idsdrr-d856f70748a7.json')
ee.Initialize(credentials)

date_start = '2022-02-01'
date_end ='2022-03-01'

tic = time.perf_counter()
cwd = os.getcwd()
assam_rc_gdf = gpd.read_file(cwd+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')
assam_dist_gdf = gpd.read_file(cwd+'/Maps/assam_district_35.geojson')

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

assam_rcs = ee.FeatureCollection("projects/ee-idsdrr/assets/assam_rc_180")
geometry = assam_rcs.geometry() 

# Get GEE Image Collection
GCN250_Average =  ee.Image("users/jaafarhadi/GCN250/GCN250Average")
GCN250_Dry =  ee.Image("users/jaafarhadi/GCN250/GCN250Dry")
GCN250_Wet = ee.Image("users/jaafarhadi/GCN250/GCN250Wet")


print("------- Images -------------")
geemap.ee_export_image(GCN250_Average,
                       filename=cwd+'/Sources/GCN250/data/GCN250_Average.tif',
                       scale=250,
                       region=geometry,
                       file_per_band=True)

geemap.ee_export_image(GCN250_Dry,
                       filename=cwd+'/Sources/GCN250/data/GCN250_Dry.tif',
                       scale=250,
                       region=geometry,
                       file_per_band=True)

geemap.ee_export_image(GCN250_Wet,
                       filename=cwd+'/Sources/GCN250/data/GCN250_Wet.tif',
                       scale=250,
                       region=geometry,
                       file_per_band=True)


print("------- Stats-------------")
# AVERAGE
gcn_avg_raster = rasterio.open(cwd+'/Sources/GCN250/data/GCN250_Average.b1.tif')

gcn_rc_df, gcn_rc_gdf = zonal_stats_choropleths(assam_rc_gdf,'object_id',
                                                   gcn_avg_raster)

#gcn_dist_df, gcn_dist_gdf = zonal_stats_choropleths(assam_dist_gdf, 'assam_dist',
#                                                   gcn_avg_raster)
gcn_rc_df.to_csv(cwd+'/Sources/GCN250/data/gcn250_average_rc.csv',
                index=False)
gcn_rc_gdf.to_file(cwd+'/Sources/GCN250/data/gcn250_average_rc.geojson')

# gcn_dist_df.to_csv(cwd+'/Sources/GCN250/data/gcn250_average_dist.csv',
#                 index=False)
# gcn_dist_gdf.to_file(cwd+'/Sources/GCN250/data/gcn250_average_dist.geojson'))


#DRY
gcn_dry_raster = rasterio.open(cwd+'/Sources/GCN250/data/GCN250_Dry.b1.tif')

gcn_rc_df, gcn_rc_gdf = zonal_stats_choropleths(assam_rc_gdf,'object_id',
                                                   gcn_dry_raster)

#gcn_dist_df, gcn_dist_gdf = zonal_stats_choropleths(assam_dist_gdf, 'assam_dist',
#                                                   gcn_dry_raster)
gcn_rc_df.to_csv(cwd+'/Sources/GCN250/data/gcn250_dry_rc.csv',
                index=False)
gcn_rc_gdf.to_file(cwd+'/Sources/GCN250/data/gcn250_dry_rc.geojson')

# gcn_dist_df.to_csv(cwd+'/Sources/GCN250/data/gcn250_dry_dist.csv',
#                 index=False)
# gcn_dist_gdf.to_file(cwd+'/Sources/GCN250/data/gcn250_dry_dist.geojson'))

#WET
gcn_wet_raster = rasterio.open(cwd+'/Sources/GCN250/data/GCN250_Wet.b1.tif')

gcn_rc_df, gcn_rc_gdf = zonal_stats_choropleths(assam_rc_gdf,'object_id',
                                                   gcn_wet_raster)

#gcn_dist_df, gcn_dist_gdf = zonal_stats_choropleths(assam_dist_gdf, 'assam_dist',
#                                                   gcn_wet_raster)
gcn_rc_df.to_csv(cwd+'/Sources/GCN250/data/gcn250_wet_rc.csv',
                index=False)
gcn_rc_gdf.to_file(cwd+'/Sources/GCN250/data/gcn250_wet_rc.geojson')

# gcn_dist_df.to_csv(cwd+'/Sources/GCN250/data/gcn250_wet_dist.csv',
#                 index=False)
# gcn_dist_gdf.to_file(cwd+'/Sources/GCN250/data/gcn250_wet_dist.geojson'))

toc = time.perf_counter()
print("Time Taken: {} seconds".format(toc-tic))