import pandas as pd
import geopandas as gpd
import os

cwd = os.getcwd()
health_centres_gdf = gpd.read_file(cwd+'/Sources/BHARATMAPS/data/RawData/BharatMaps_HealthCenters.geojson')
assam_rc_gdf = gpd.read_file(cwd+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')

health_centres_in_rcs = gpd.sjoin(assam_rc_gdf, health_centres_gdf.to_crs(assam_rc_gdf.crs), how="left", predicate="contains")
health_centres_count = health_centres_in_rcs.groupby('object_id').size().reset_index(name='health_centres_count')

health_centres_count.to_csv(cwd+'/Sources/BHARATMAPS/data/variables/healthcentres_per_rc.csv', index=False)