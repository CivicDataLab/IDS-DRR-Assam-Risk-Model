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
for month in tqdm(hazard_df.timeperiod.unique()):
    hazard_df_month = hazard_df[hazard_df.timeperiod == month]
    
    # Define the corresponding categories
    #categories = ['very low', 'low', 'medium', 'high', 'very high']
    categories = [1, 2, 3, 4, 5]

    # Calculate mean and standard deviation
    mean = hazard_df_month['drainage_density'].mean()
    std = hazard_df_month['drainage_density'].std()
    
    # Define the conditions for each category
    conditions = [
        (hazard_df_month['drainage_density'] <= mean),
        (hazard_df_month['drainage_density'] > mean) & (hazard_df_month['drainage_density'] <= mean + std),
        (hazard_df_month['drainage_density'] > mean + std) & (hazard_df_month['drainage_density'] <= mean + 2 * std),
        (hazard_df_month['drainage_density'] > mean + 2 * std) & (hazard_df_month['drainage_density'] <= mean + 3 * std),
        (hazard_df_month['drainage_density'] > mean + 3 * std)
    ]
    # Create the new column based on the conditions
    hazard_df_month['drainage_density_level'] = np.select(conditions, categories, default='outlier')

    #!! ************** !!#
    # Calculate mean and standard deviation
    mean = hazard_df_month['mean_rain'].mean()
    std = hazard_df_month['mean_rain'].std()
    
    # Define the conditions for each category
    conditions = [
        (hazard_df_month['mean_rain'] <= mean),
        (hazard_df_month['mean_rain'] > mean) & (hazard_df_month['mean_rain'] <= mean + std),
        (hazard_df_month['mean_rain'] > mean + std) & (hazard_df_month['mean_rain'] <= mean + 2 * std),
        (hazard_df_month['mean_rain'] > mean + 2 * std) & (hazard_df_month['mean_rain'] <= mean + 3 * std),
        (hazard_df_month['mean_rain'] > mean + 3 * std)
    ]
    # Create the new column based on the conditions
    hazard_df_month['mean_rain_level'] = np.select(conditions, categories, default='outlier')
    #!! ************** !!#
    # Calculate mean and standard deviation
    mean = hazard_df_month['max_rain'].mean()
    std = hazard_df_month['max_rain'].std()
    
    # Define the conditions for each category
    conditions = [
        (hazard_df_month['max_rain'] <= mean),
        (hazard_df_month['max_rain'] > mean) & (hazard_df_month['max_rain'] <= mean + std),
        (hazard_df_month['max_rain'] > mean + std) & (hazard_df_month['max_rain'] <= mean + 2 * std),
        (hazard_df_month['max_rain'] > mean + 2 * std) & (hazard_df_month['max_rain'] <= mean + 3 * std),
        (hazard_df_month['max_rain'] > mean + 3 * std)
    ]
    # Create the new column based on the conditions
    hazard_df_month['max_rain_level'] = np.select(conditions, categories, default='outlier')
    #!! ************** !!#
    
    # Calculate mean and standard deviation
    mean = hazard_df_month['inundation_intensity_mean_nonzero'].mean()
    std = hazard_df_month['inundation_intensity_mean_nonzero'].std()
    
    # Define the conditions for each category
    conditions = [
        (hazard_df_month['inundation_intensity_mean_nonzero'] <= mean),
        (hazard_df_month['inundation_intensity_mean_nonzero'] > mean) & (hazard_df_month['inundation_intensity_mean_nonzero'] <= mean + std),
        (hazard_df_month['inundation_intensity_mean_nonzero'] > mean + std) & (hazard_df_month['inundation_intensity_mean_nonzero'] <= mean + 2 * std),
        (hazard_df_month['inundation_intensity_mean_nonzero'] > mean + 2 * std) & (hazard_df_month['inundation_intensity_mean_nonzero'] <= mean + 3 * std),
        (hazard_df_month['inundation_intensity_mean_nonzero'] > mean + 3 * std)
    ]
    # Create the new column based on the conditions
    hazard_df_month['inundation_intensity_mean_nonzero_level'] = np.select(conditions, categories, default='outlier')
    #!! ************** !!#

    # Calculate mean and standard deviation
    mean = hazard_df_month['inundation_intensity_sum'].mean()
    std = hazard_df_month['inundation_intensity_sum'].std()

    # Define the conditions for each category
    conditions = [
        (hazard_df_month['inundation_intensity_sum'] <= mean),
        (hazard_df_month['inundation_intensity_sum'] > mean) & (hazard_df_month['inundation_intensity_sum'] <= mean + std),
        (hazard_df_month['inundation_intensity_sum'] > mean + std) & (hazard_df_month['inundation_intensity_sum'] <= mean + 2 * std),
        (hazard_df_month['inundation_intensity_sum'] > mean + 2 * std) & (hazard_df_month['inundation_intensity_sum'] <= mean + 3 * std),
        (hazard_df_month['inundation_intensity_sum'] > mean + 3 * std)
    ]
    
    # Create the new column based on the conditions
    hazard_df_month['inundation_intensity_sum_level'] = np.select(conditions, categories, default='outlier')
    #!! ************** !!#

    #Average of all levels
    hazard_df_month['flood-hazard'] = (hazard_df_month['inundation_intensity_mean_nonzero_level'].astype(int)
                                        + hazard_df_month['inundation_intensity_sum_level'].astype(int)
                                        + hazard_df_month['mean_rain_level'].astype(int)
                                        + hazard_df_month['max_rain_level'].astype(int)
                                        + hazard_df_month['drainage_density_level'].astype(int))/5
    
    hazard_df_month['flood-hazard'] = round(hazard_df_month['flood-hazard'])

    hazard_df_months.append(hazard_df_month)

hazard = pd.concat(hazard_df_months)

master_variables = master_variables.merge(hazard[['timeperiod', 'object_id', 'flood-hazard']],
                       on = ['timeperiod', 'object_id'])

master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_flood-hazard.csv', index=False)