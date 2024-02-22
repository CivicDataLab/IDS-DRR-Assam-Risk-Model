import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm 
import os
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

master_variables = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/MASTER_VARIABLES.csv')

def get_financial_year(timeperiod):
    if int(timeperiod.split('_')[1]) >= 4:
        return str(int(timeperiod.split('_')[0]))+'-'+str(int(timeperiod.split('_')[0])+1)
    else:
        return str(int(timeperiod.split('_')[0]) - 1)+'-'+str(int(timeperiod.split('_')[0]))
    
# Apply the function to create the 'FinancialYear' column
master_variables['FinancialYear'] = master_variables['timeperiod'].apply(lambda x: get_financial_year(x))

#INPUT VARS
government_response_vars = ["total_tender_awarded_value",
                       #"SOPD_tenders_awarded_value",
                       "SDRF_tenders_awarded_value",
                       #"RIDF_tenders_awarded_value",
                       #"LTIF_tenders_awarded_value",
                    #   "CIDF_tenders_awarded_value",
                    #   "Preparedness Measures_tenders_awarded_value",
                    #   "Immediate Measures_tenders_awarded_value",
                    #   "Others_tenders_awarded_value"
                      ]

# Find cumsum in each FY of the government response vars
for var in government_response_vars:
    master_variables[var]=master_variables.groupby(['object_id','FinancialYear'])[var].cumsum()


govtresponse_df = master_variables[government_response_vars + ['timeperiod', 'object_id']]


govtresponse_df_months = []
for month in tqdm(govtresponse_df.timeperiod.unique()):
    govtresponse_df_month = govtresponse_df[govtresponse_df.timeperiod == month]
    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    # Fit scaler to the data and transform it
    govtresponse_df_month[government_response_vars] = scaler.fit_transform(govtresponse_df_month[government_response_vars])
    
    # Sum scaled exposure vars
    govtresponse_df_month['sum'] = govtresponse_df_month[government_response_vars].sum(axis=1)

    # Calculate mean and standard deviation
    mean = govtresponse_df_month['sum'].mean()
    std = govtresponse_df_month['sum'].std()
    
    # Define the conditions for each category
    conditions = [
        (govtresponse_df_month['sum'] <= mean),
        (govtresponse_df_month['sum'] > mean) & (govtresponse_df_month['sum'] <= mean + std),
        (govtresponse_df_month['sum'] > mean + std) & (govtresponse_df_month['sum'] <= mean + 2 * std),
        (govtresponse_df_month['sum'] > mean + 2 * std) & (govtresponse_df_month['sum'] <= mean + 3 * std),
        (govtresponse_df_month['sum'] > mean + 3 * std)
    ]
    
    # Define the corresponding categories
    #categories = ['very low', 'low', 'medium', 'high', 'very high']
    categories = [5, 4, 3, 2, 1]
    
    # Create the new column based on the conditions
    govtresponse_df_month['government-response'] = np.select(conditions, categories, default='outlier')

    govtresponse_df_months.append(govtresponse_df_month)

govtresponse = pd.concat(govtresponse_df_months)
master_variables = master_variables.merge(govtresponse[['timeperiod', 'object_id', 'government-response']],
                       on = ['timeperiod', 'object_id'])

master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_government-response.csv', index=False)