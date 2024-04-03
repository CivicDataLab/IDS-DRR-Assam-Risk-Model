#FINAL DATASET FOR ARCHIT
import pandas as pd
import glob

files = glob.glob('LDA/data/*.csv')
master_df = pd.read_csv('MASTER_VARIABLES.csv')
print(master_df.shape)
print('/n')
dfs = []
for file in files:
    df = pd.read_csv(file)
    df['object_id'] = df['object_id'].apply(lambda x: round(x))
    dfs.append(master_df.merge(df[['object_id', 'timeperiod',
                      'fldhzrdscore', 'exposurescore', 'infrascore', 'impact', 'respscore', 'Topsis_Score',
                        'compositescore_grp', 'Rank', 'fldhzrdscore_un', 'exposurescore_un', 'infrascore_un', 'impact_un', 'respscore_un']],
                     on=['object_id', 'timeperiod']))

MASTER = pd.concat(dfs)
MASTER = master_df.merge(MASTER[['object_id', 'timeperiod',
                      'fldhzrdscore', 'exposurescore', 'infrascore', 'impact', 'respscore', 'Topsis_Score',
                        'compositescore_grp', 'Rank', 'fldhzrdscore_un', 'exposurescore_un', 'infrascore_un', 'impact_un', 'respscore_un']],
                     on=['object_id', 'timeperiod'],
                     how='left')


# ROUND
MASTER['sum_rain'] = MASTER['sum_rain'].apply(lambda x: round(x,2))
MASTER['inundation_intensity_mean'] = MASTER['inundation_intensity_mean'].apply(lambda x: round(x,2))
MASTER['riverlevel_mean'] = MASTER['riverlevel_mean'].apply(lambda x: round(x,2))
MASTER['elevation_mean'] = MASTER['elevation_mean'].apply(lambda x: round(x))
MASTER['sum_population'] = MASTER['sum_population'].apply(lambda x: round(x))
MASTER['road_length'] = MASTER['road_length'].apply(lambda x: round(x,2))
MASTER['rail_length'] = MASTER['rail_length'].apply(lambda x: round(x,2))


#SEX RATIO
MASTER['sum-male-population'] = MASTER['sum_population']/(1+MASTER['mean_sexratio'])
MASTER['sum-male-population'] = MASTER['sum-male-population'].apply(lambda x: round(x))

MASTER['sum-female-population'] = MASTER['sum_population'] - MASTER['sum-male-population']
MASTER['mean_sexratio'] = MASTER['mean_sexratio']*1000
MASTER['mean_sexratio'] = MASTER['mean_sexratio'].apply(lambda x: round(x))

#RENAME COLUMNS FOR FRONTEND
new_column_names = {'respscore_un': 'government-response',
                    'total_tender_awarded_value': 'total-tender-awarded-value',
                    'SDRF_tenders_awarded_value': 'SDRF-tenders-awarded-value',
                    'Preparedness Measures_tenders_awarded_value': 'restoration-measures-tenders-awarded-value',
                    'Immediate Measures_tenders_awarded_value': 'immediate-measures-tenders-awarded-value',

                    'impact_un': 'damages-losses',
                    'Population_affected_Total': 'population-affected-total',
                    'Crop_Area': 'crop-area',
                    'Total_House_Fully_Damaged': 'total-house-fully-damaged',
                    'Human_Live_Lost': 'human-live-lost',

                    'infrascore_un': 'vulnerability',
                    'schools_count': 'schools-count',
                    'health_centres_count': 'health-centres-count',
                    'road_length': 'road-length',
                    'net_sown_area_in_hac': 'net-sown-area-in-hac',

                    'exposurescore_un': 'exposure',
                    'sum-male-population': 'sum-male-population',
                    'sum-female-population': 'sum-female-population',
                    'total_hhd': 'households',
                    'sum_population': 'sum-population',

                    'fldhzrdscore_un': 'flood-hazard',
                    'sum_rain': 'sum-rain',
                    'inundation_intensity_mean': 'inundation-intensity-mean',
                    'riverlevel_mean': 'riverlevel-mean',
                    'elevation_mean': 'elevation-mean',

                    'compositescore_grp': 'composite-score'

                    }


MASTER.rename(columns=new_column_names, inplace=True)
MASTER['year'] = MASTER['timeperiod'].str[:4]
MASTER['year'] = MASTER['year'].astype(int)
MASTER['month'] = MASTER['timeperiod'].str[5:]
MASTER['month'] = MASTER['month'].astype(int)
MASTER.to_csv('MASTER_DATA_FRONTEND_ALLMONTHS.csv', index=False)
MASTER[MASTER['year'].isin([2022, 2023])].to_csv('MASTER_DATA_FRONTEND_2022onwards.csv', index=False)
