import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point # Shapely for converting latitude/longtitude to geometry
import os
import urllib3
urllib3.disable_warnings()

path = os.getcwd()+'/Sources/FFS'

assam_stations_gdf = gpd.read_file(path+'/data/assam_stations.geojson')

startDate = '2018-01-01'
endDate = '2023-09-30'

master_df = pd.read_csv(path+'/data/Waterlevel_assam_stations.csv')
for stationCode in list(assam_stations_gdf.stationCode):
    print(stationCode)
    dynamic_url = 'https://ffs.india-water.gov.in/iam/api/new-entry-data/specification/sorted?sort-criteria=%7B%22sortOrderDtos%22:%5B%7B%22sortDirection%22:%22ASC%22,%22field%22:%22id.dataTime%22%7D%5D%7D&specification=%7B%22where%22:%7B%22where%22:%7B%22where%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.stationCode%22,%22operator%22:%22eq%22,%22value%22:%22'+stationCode+'%22%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.datatypeCode%22,%22operator%22:%22eq%22,%22value%22:%22HHS%22%7D%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22dataValue%22,%22operator%22:%22null%22,%22value%22:%22false%22%7D%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.dataTime%22,%22operator%22:%22btn%22,%22value%22:%22'+startDate+'T16:49:44.574,'+endDate+'T16:49:44.574%22%7D%7D%7D'
    r = requests.get(dynamic_url,verify=False)
    txt = r.json()
    df = pd.DataFrame(txt)
    try:
          df['Date'] = df.id.apply(lambda x: x['dataTime'].split('T')[0])
          df['Time'] = df.id.apply(lambda x: x['dataTime'].split('T')[1])
          df = df[['stationCode','Date','Time','dataValue','datatypeCode']]
          master_df = pd.concat([master_df,df],ignore_index=True)
          master_df = master_df.drop_duplicates()
          master_df.to_csv(path+'/data/Waterlevel_assam_stations.csv',index=False)
    except:
         print('No data available in given time period at: ', stationCode)
         continue


