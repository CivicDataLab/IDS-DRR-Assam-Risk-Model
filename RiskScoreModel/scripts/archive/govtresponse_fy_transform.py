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
master_variables['financial_year'] = master_variables['timeperiod'].apply(lambda x: get_financial_year(x))

#INPUT VARS
government_response_vars = ["total_tender_awarded_value",
                            #"total_expenditure_value",
                       #"SOPD_tenders_awarded_value",
                       "SDRF_sanctions_awarded_value",
                       "SDRF_tenders_awarded_value",
                       #"RIDF_tenders_awarded_value",
                       #"LTIF_tenders_awarded_value",
                    #   "CIDF_tenders_awarded_value",
                       "Preparedness Measures_tenders_awarded_value",
                       "Immediate Measures_tenders_awarded_value",
                       "Others_tenders_awarded_value"
                      ]

government_response_indicators = ["total_tender_awarded_value",
                            #"total_expenditure_value",
                       #"SOPD_tenders_awarded_value",
                       "SDRF_sanctions_awarded_value",
                       "SDRF_tenders_awarded_value",
                       #"RIDF_tenders_awarded_value",
                       #"LTIF_tenders_awarded_value",
                    #   "CIDF_tenders_awarded_value",
                    #   "Preparedness Measures_tenders_awarded_value",
                    #   "Immediate Measures_tenders_awarded_value",
                    #   "Others_tenders_awarded_value"
                      ]

# Find cumsum in each FY of the government response vars
# Reset indicators at the start of each financial year, cumulative sum monthly
master_variables.sort_values(by=['object_id', 'financial_year', 'timeperiod'], inplace=True)

# Reset government response vars to zero at the start of each financial year
for var in government_response_vars:
    master_variables[var + '_fy_cumsum'] = master_variables.groupby(['object_id', 'financial_year'])[var].cumsum()

# Now use the cumulative variables for normalization and score calculations
govtresponse_df = master_variables[[var + '_fy_cumsum' for var in government_response_indicators] + ['timeperiod', 'object_id']]

govtresponse_df_months = []
for month in tqdm(govtresponse_df.timeperiod.unique()):
    govtresponse_df_month = govtresponse_df[govtresponse_df.timeperiod == month].copy()
    
    scaler = MinMaxScaler()
    cumsum_vars = [var + '_fy_cumsum' for var in government_response_indicators]

    govtresponse_df_month[cumsum_vars] = scaler.fit_transform(govtresponse_df_month[cumsum_vars])
    
    govtresponse_df_month['sum'] = govtresponse_df_month[cumsum_vars].sum(axis=1)

    mean = govtresponse_df_month['sum'].mean()
    std = govtresponse_df_month['sum'].std()
    
    conditions = [
        (govtresponse_df_month['sum'] <= mean),
        (govtresponse_df_month['sum'] > mean) & (govtresponse_df_month['sum'] <= mean + std),
        (govtresponse_df_month['sum'] > mean + std) & (govtresponse_df_month['sum'] <= mean + 2 * std),
        (govtresponse_df_month['sum'] > mean + 2 * std) & (govtresponse_df_month['sum'] <= mean + 3 * std),
        (govtresponse_df_month['sum'] > mean + 3 * std)
    ]
    
    categories = [5, 4, 3, 2, 1]
    
    govtresponse_df_month['government-response'] = np.select(conditions, categories, default='outlier')

    govtresponse_df_months.append(govtresponse_df_month)

govtresponse = pd.concat(govtresponse_df_months)

master_variables = master_variables.merge(govtresponse[['timeperiod', 'object_id', 'government-response']],
                                          on=['timeperiod', 'object_id'])

master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_government-response_2.csv', index=False)
