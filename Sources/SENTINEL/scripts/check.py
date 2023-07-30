import geopandas as gpd
import pandas as pd

import os

cwd = os.getcwd()
date_end ='2022-09-01'

ndvi_df = pd.read_csv(cwd+'/Sources/SENTINEL/data/ndvi_{}.csv'.format(date_end))
ndbi_df = pd.read_csv(cwd+'/Sources/SENTINEL/data/ndbi_{}.csv'.format(date_end))

assam_rc = gpd.read_file(cwd+'/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp')

