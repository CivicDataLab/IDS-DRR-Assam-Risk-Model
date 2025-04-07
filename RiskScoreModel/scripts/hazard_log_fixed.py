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

# Method 2: Log Transformation with Quantile Binning
def log_quantile_binning(df, var):
    """
    Perform log transformation and quantile binning on a variable.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        var (str): Variable name to transform and bin
        
    Returns:
        pd.Series: Binned values from 1 to 5
    """
    # Add a small constant to avoid log(0)
    log_var = np.log1p(df[var])
    
    # Get quantile bins without labels first
    bins = pd.qcut(log_var, q=5, labels=False, duplicates='drop')
    
    # Add 1 to shift from 0-4 to 1-5
    return bins + 1

for month in tqdm(hazard_df.timeperiod.unique()):
    hazard_df_month = hazard_df[hazard_df.timeperiod == month].copy()
    
    # Apply custom binning based on value ranges
    hazard_df_month['drainage_density_custom'] = log_quantile_binning(hazard_df_month, 'drainage_density')
    hazard_df_month['mean_rain_custom'] = log_quantile_binning(hazard_df_month, 'mean_rain')
    hazard_df_month['max_rain_custom'] = log_quantile_binning(hazard_df_month, 'max_rain')
    hazard_df_month['inundation_intensity_mean_nonzero_custom'] = log_quantile_binning(hazard_df_month, 'inundation_intensity_mean_nonzero')
    hazard_df_month['inundation_intensity_sum_custom'] = log_quantile_binning(hazard_df_month, 'inundation_intensity_sum')
    
    # Average hazard score
    hazard_df_month['flood-hazard-float'] = (hazard_df_month[['drainage_density_custom', 'mean_rain_custom', 
                                                        'max_rain_custom', 'inundation_intensity_mean_nonzero_custom',
                                                        'inundation_intensity_sum_custom']]
                                       .astype(float).mean(axis=1))

    hazard_df_month['flood-hazard'] = round(hazard_df_month['flood-hazard-float'])
    
    hazard_df_months.append(hazard_df_month)

hazard = pd.concat(hazard_df_months)
master_variables = master_variables.merge(hazard[['timeperiod', 'object_id', 'flood-hazard']],
                       on=['timeperiod', 'object_id'])

master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_flood-hazard.csv', index=False)