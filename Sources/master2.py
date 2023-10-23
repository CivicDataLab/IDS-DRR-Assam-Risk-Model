import pandas as pd
import os
import glob
import datetime
import geopandas as gpd
import warnings
warnings.filterwarnings("ignore")

variables_data_path = os.getcwd() + '/Sources/master/'
assam_rc = gpd.read_file('Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.geojson')

date_range = pd.date_range(start="2021-05-01", end="2023-08-01", freq='MS')

# Format the date values as "YYYY_MM" strings
formatted_dates = [date.strftime('%Y_%m') for date in date_range]

# Create a Pandas DataFrame with the values
dfs = []
for year_month in formatted_dates:
    df = assam_rc[['object_id']]
    df['timeperiod'] = year_month
    dfs.append(df)
master_df =  pd.concat(dfs).reset_index(drop = True)
#df = pd.DataFrame({'timeperiod': formatted_dates})

# Variables for model input
monthly_variables = ['total_tender_awarded_value',
                     'SOPD_tenders_awarded_value', 'SDRF_tenders_awarded_value', 'RIDF_tenders_awarded_value', 'LTIF_tenders_awarded_value', 'CIDF_tenders_awarded_value',
                      'Preparedness Measures_tenders_awarded_value', 'Immediate Measures_tenders_awarded_value', 'Others_tenders_awarded_value',
                      'Total_Animal_Washed_Away', 'Total_Animal_Affected',
                      'Population_affected_Total',
                      'Male_Camp', 'Female_Camp', 'Children_Camp',
                     'Total_House_Fully_Damaged',
                     'Human_Live_Lost_Children', 'Human_Live_Lost_Female', 'Human_Live_Lost_Male',
                     'Embankments affected', 'Roads', 'Bridge', 'Embankment breached',
                     'rainfall',
                     'mean_ndvi', 'mean_ndbi',
                     'inundation_pct', 'riverlevel'
                     ]

for variable in monthly_variables:
    variable_df = pd.read_csv(variables_data_path + variable + '.csv')
    variable_df = variable_df.drop_duplicates()
    master_df = master_df.merge(variable_df, on=['object_id', 'timeperiod'], how='left')

master_df['Relief_Camp_inmates'] = master_df['Male_Camp'].fillna(0).astype(int) \
    + master_df['Female_Camp'].fillna(0).astype(int) \
    + master_df['Children_Camp'].fillna(0).astype(int)

master_df['Human_Live_Lost'] = master_df['Human_Live_Lost_Children'].fillna(0).astype(int) \
    + master_df['Human_Live_Lost_Female'].fillna(0).astype(int) \
    + master_df['Human_Live_Lost_Male'].fillna(0).astype(int)


master_df = master_df.drop(['Male_Camp', 'Female_Camp', 'Children_Camp',
                            'Human_Live_Lost_Male', 'Human_Live_Lost_Children', 'Human_Live_Lost_Female'], axis=1)


# Annual variables
master_df['year'] = master_df['timeperiod'].str[:4].astype(int)
annual_variables = ['mean_sexratio', 'sum_aged_population', 'sum_young_population', 'sum_population']

for variable in annual_variables:
    variable_df = pd.read_csv(variables_data_path + variable + '.csv')
    variable_df = variable_df.rename(columns = {'timeperiod': 'year'})
    master_df = master_df.merge(variable_df,
                                on = ['object_id', 'year'],
                                how='left')

# one-time variables
onetime_variables = ['Schools', 'HealthCenters', 'RailLengths', 'RoadLengths', 'gcn250_average', 'elevation', 'antyodaya_variables']
master_df['year'] = ''

for variable in onetime_variables:
    variable_df = pd.read_csv(variables_data_path + variable + '.csv')
    variable_df = variable_df.rename(columns = {'timeperiod': 'year'})
    variable_df['year'] = ''
    master_df = master_df.merge(variable_df,
                                on = ['object_id', 'year'],
                                how='left')


master_df = master_df.drop(['year', 'count_gcn250_pixels',
                            'count_bhuvan_pixels', 'count_inundated_pixels'], axis=1)

#master_df['year'] = master_df['timeperiod'].str[:4]
#master_df['month'] = master_df['timeperiod'].str[-2:]


# Missing data imputation
master_df['total_tender_awarded_value'] = master_df['total_tender_awarded_value'].fillna(0)
master_df['SOPD_tenders_awarded_value'] = master_df['SOPD_tenders_awarded_value'].fillna(0)
master_df['SDRF_tenders_awarded_value'] = master_df['SDRF_tenders_awarded_value'].fillna(0)
master_df['RIDF_tenders_awarded_value'] = master_df['RIDF_tenders_awarded_value'].fillna(0)
master_df['LTIF_tenders_awarded_value'] = master_df['LTIF_tenders_awarded_value'].fillna(0)
master_df['CIDF_tenders_awarded_value'] = master_df['CIDF_tenders_awarded_value'].fillna(0)
master_df['Preparedness Measures_tenders_awarded_value'] = master_df['Preparedness Measures_tenders_awarded_value'].fillna(0)
master_df['Immediate Measures_tenders_awarded_value'] = master_df['Immediate Measures_tenders_awarded_value'].fillna(0)
master_df['Others_tenders_awarded_value'] = master_df['Others_tenders_awarded_value'].fillna(0)


master_df['Population_affected_Total'] = master_df['Population_affected_Total'].fillna(0)
master_df['Total_Animal_Affected'] = master_df['Total_Animal_Affected'].fillna(0)
master_df['Total_Animal_Washed_Away'] = master_df['Total_Animal_Washed_Away'].fillna(0)
master_df['Total_House_Fully_Damaged'] = master_df['Total_House_Fully_Damaged'].fillna(0)
master_df['Roads'] = master_df['Roads'].fillna(0)
master_df['Embankments affected'] = master_df['Embankments affected'].fillna(0)
master_df['Bridge'] = master_df['Bridge'].fillna(0)
master_df['Embankment breached'] = master_df['Embankment breached'].fillna(0)

#mean of rc
master_df['mean_ndvi'] = master_df['mean_ndvi'].fillna(master_df.groupby(['object_id'])['mean_ndvi'].transform('mean'))
master_df['ndbi_mean'] = master_df['ndbi_mean'].fillna(master_df.groupby(['object_id'])['ndbi_mean'].transform('mean'))
master_df['max_rain'] = master_df['max_rain'].fillna(master_df.groupby(['object_id'])['max_rain'].transform('mean'))
master_df['mean_rain'] = master_df['mean_rain'].fillna(master_df.groupby(['object_id'])['mean_rain'].transform('mean'))
master_df['sum_rain'] = master_df['sum_rain'].fillna(master_df.groupby(['object_id'])['sum_rain'].transform('mean'))

master_df.to_csv('MASTER_VARIABLES.csv', index=False)

#master_df[master_df.duplicated(subset= ['object_id', 'timeperiod'])].to_csv('MASTER_VARIABLES.csv', index=False)