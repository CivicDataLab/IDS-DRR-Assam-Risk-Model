import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm 
import os
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

master_variables = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/MASTER_VARIABLES.csv')

exposure_vars = ['sum_population', 'total_hhd']

exposure_df = master_variables[exposure_vars + ['timeperiod', 'object_id']]


exposure_df_months = []
for month in tqdm(exposure_df.timeperiod.unique()):
    exposure_df_month = exposure_df[exposure_df.timeperiod == month]
    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    # Fit scaler to the data and transform it
    exposure_df_month[exposure_vars] = scaler.fit_transform(exposure_df_month[exposure_vars])
    
    # Sum scaled exposure vars
    
    exposure_df_month['sum'] = exposure_df_month[exposure_vars].sum(axis=1)
    
    # Calculate mean and standard deviation
    mean = exposure_df_month['sum'].mean()
    std = exposure_df_month['sum'].std()
    
    # Define the conditions for each category
    conditions = [
        (exposure_df_month['sum'] <= mean),
        (exposure_df_month['sum'] > mean) & (exposure_df_month['sum'] <= mean + std),
        (exposure_df_month['sum'] > mean + std) & (exposure_df_month['sum'] <= mean + 2 * std),
        (exposure_df_month['sum'] > mean + 2 * std) & (exposure_df_month['sum'] <= mean + 3 * std),
        (exposure_df_month['sum'] > mean + 3 * std)
    ]
    
    # Define the corresponding categories
    #categories = ['very low', 'low', 'medium', 'high', 'very high']
    categories = [1, 2, 3, 4, 5]
    
    # Create the new column based on the conditions
    exposure_df_month['exposure'] = np.select(conditions, categories, default='outlier')

    exposure_df_months.append(exposure_df_month)

exposure = pd.concat(exposure_df_months)

master_variables = master_variables.merge(exposure[['timeperiod', 'object_id', 'exposure']],
                       on = ['timeperiod', 'object_id'])

master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_exposure.csv', index=False)