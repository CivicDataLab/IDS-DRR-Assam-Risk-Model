import pandas as pd
import os
import geopandas as gpd
path = os.getcwd()+'/Sources/FFS'

ffs_df = pd.read_csv(path+'/data/Waterlevel_assam_stations.csv')
ffs_df['year_month'] = ffs_df.Date.str[:4] + '_' + ffs_df.Date.str[5:7]

assam_stations = gpd.read_file(path+'/data/assam_stations.geojson')
assam_rc = gpd.read_file('Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.geojson')

result = gpd.sjoin(assam_stations[['stationCode','geometry']], assam_rc[['object_id','revenue_ci','geometry']])

# DAILY RIVER LEVELS
grouped_df = ffs_df.groupby(['stationCode','Date']).agg({'dataValue': ['mean', 'min', 'max']}) 
grouped_df = grouped_df.reset_index()
grouped_df.columns = ['stationCode', 'Date', 'riverlevel_mean', 'riverlevel_min', 'riverlevel_max']
grouped_df = grouped_df.merge(result[['stationCode','object_id','revenue_ci']], on='stationCode')
grouped_df.to_csv(path+'/data/variables/riverlevel_daily.csv', index=False)

# MONTHLY RIVER LEVELS - MASTER
grouped_df = ffs_df.merge(result[['stationCode','object_id','revenue_ci']], on='stationCode')
grouped_df = grouped_df.groupby(['object_id','year_month']).agg({'dataValue': ['mean', 'min', 'max']}) 
grouped_df = grouped_df.reset_index()
grouped_df.columns = ['object_id', 'timeperiod', 'riverlevel_mean', 'riverlevel_min', 'riverlevel_max']
grouped_df.to_csv(os.getcwd() + '/Sources/master/riverlevel.csv', index=False)
