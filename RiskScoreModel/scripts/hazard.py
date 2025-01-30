import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm 
import os
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

master_variables = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/MASTER_VARIABLES.csv')
hazard_vars = ['inundation_intensity_mean_nonzero', 'inundation_intensity_sum', 'drainage_density', 'mean_rain', 'max_rain']
hazard_df = master_variables[hazard_vars + ['timeperiod', 'object_id']]
hazard_df_months = []


# Define categories for hazard levels
categories = [1, 2, 3, 4, 5]
def custom_binning(df, var):
    conditions = [
        (df[var] == 0),
        (df[var] > 0) & (df[var] <= df[var].quantile(0.25)),
        (df[var] > df[var].quantile(0.25)) & (df[var] <= df[var].quantile(0.5)),
        (df[var] > df[var].quantile(0.5)) & (df[var] <= df[var].quantile(0.75)),
        (df[var] > df[var].quantile(0.75))
    ]
    return np.select(conditions, categories, default='outlier')


for month in tqdm(hazard_df.timeperiod.unique()):
    hazard_df_month = hazard_df[hazard_df.timeperiod == month]
    
    # Apply custom binning based on value ranges
    hazard_df_month['drainage_density_custom'] = custom_binning(hazard_df_month, 'drainage_density')
    hazard_df_month['mean_rain_custom'] = custom_binning(hazard_df_month, 'mean_rain')
    hazard_df_month['max_rain_custom'] = custom_binning(hazard_df_month, 'max_rain')
    hazard_df_month['inundation_intensity_mean_nonzero_custom'] = custom_binning(hazard_df_month, 'inundation_intensity_mean_nonzero')
    hazard_df_month['inundation_intensity_sum_custom'] = custom_binning(hazard_df_month, 'inundation_intensity_sum')
    
    #Average of all levels
    
    # Average hazard score
    hazard_df_month['flood-hazard-float'] = (hazard_df_month[['drainage_density_custom', 'mean_rain_custom', 
                                                        'max_rain_custom', 'inundation_intensity_mean_nonzero_custom',
                                                        'inundation_intensity_sum_custom']]
                                       .astype(float).mean(axis=1))

    hazard_df_month['flood-hazard'] = round(hazard_df_month['flood-hazard-float'])

    hazard_df_months.append(hazard_df_month)

hazard = pd.concat(hazard_df_months)
master_variables = master_variables.merge(hazard[['timeperiod', 'object_id', 'flood-hazard']],
                       on = ['timeperiod', 'object_id'])

master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_flood-hazard.csv', index=False)