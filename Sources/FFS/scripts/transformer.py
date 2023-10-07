import pandas as pd
import os
import geopandas as gpd
path = os.getcwd()+'/Sources/FFS'

ffs_df = pd.read_csv(path+'/data/Waterlevel_assam_stations.csv')

assam_stations = gpd.read_file(path+'/data/assam_stations.geojson')
assam_rc = gpd.read_file('Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.geojson')

result = gpd.sjoin(assam_stations[['stationCode','geometry']], assam_rc[['object_id','revenue_ci','geometry']])

grouped_df = ffs_df.groupby(['stationCode','Date']).agg({'dataValue': ['mean', 'min', 'max']}) 

grouped_df = grouped_df.reset_index().reset_index(drop=True)

grouped_df = grouped_df.merge(result[['stationCode','object_id','revenue_ci']], on='stationCode')
grouped_df = grouped_df.drop('stationCode', axis=1)
grouped_df.columns = ['stationCode', 'Date', 'mean', 'min', 'max', 'object_id', 'revenue_ci']
grouped_df.to_csv(path+'/data/waterlevelstats.csv', index=False)
