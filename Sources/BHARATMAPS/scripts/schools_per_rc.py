import pandas as pd
import geopandas as gpd
import os

cwd = os.getcwd()
schools_gdf = gpd.read_file(cwd+'/Sources/BHARATMAPS/data/RawData/BharatMaps_Schools.geojson')
assam_rc_gdf = gpd.read_file(cwd+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')

schools_in_rcs = gpd.sjoin(assam_rc_gdf, schools_gdf.to_crs(assam_rc_gdf.crs), how="left", predicate="contains")
schools_count = schools_in_rcs.groupby('object_id').size().reset_index(name='schools_count')

schools_count.to_csv(cwd+'/Sources/BHARATMAPS/data/variables/Schools.csv', index=False)