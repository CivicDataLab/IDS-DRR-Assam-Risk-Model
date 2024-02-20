import numpy as np
import DEA
import pandas as pd
import os
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
import jenkspy




#df = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/government-response.csv')
master_variables = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/MASTER_VARIABLES.csv')
master_variables = master_variables.set_index('object_id')

#master_variables = master_variables.merge(df[['timeperiod', 'object_id', 'government-response']],
 #                      on = ['timeperiod', 'object_id'])

#master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_govtresponse.csv', index=False)


def get_financial_year(timeperiod):
    if int(timeperiod.split('_')[1]) >= 4:
        return str(int(timeperiod.split('_')[0]))+'-'+str(int(timeperiod.split('_')[0])+1)
    else:
        return str(int(timeperiod.split('_')[0]) - 1)+'-'+str(int(timeperiod.split('_')[0]))
    
# Apply the function to create the 'FinancialYear' column
master_variables['FinancialYear'] = master_variables['timeperiod'].apply(lambda x: get_financial_year(x))
#INPUT VARS
I = ["total_tender_awarded_value",
                      "SOPD_tenders_awarded_value",
                      "SDRF_tenders_awarded_value",
                      "RIDF_tenders_awarded_value",
                      "LTIF_tenders_awarded_value",
                      "CIDF_tenders_awarded_value",
                      "Preparedness Measures_tenders_awarded_value",
                      "Immediate Measures_tenders_awarded_value",
                      "Others_tenders_awarded_value"
                      ]

# Find cumsum in each FY of the government response vars
for var in I:
    master_variables[var]=master_variables.groupby(['object_id','FinancialYear'])[var].cumsum()

#OUTPUT VARS
J = ["Total_Animal_Affected","Population_affected_Total",
                "Crop_Area","Total_House_Fully_Damaged","Embankments affected",
                 "Roads","Bridge"]

K = list(master_variables.index.unique())

master_variables = master_variables[master_variables['timeperiod']=='2022_10']

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import os

X = {}
for col in I:
    X[col] = master_variables[col].to_dict()

Y = {}
for col in J:
    Y[col] = master_variables[col].to_dict()

# CRS_DEA_Model        
def getOverallEfficiency(r):

    # Model Building
    model = LpProblem('CRS_model', LpMinimize) # 建立一個新的model，命名為model
    
    # Decision variables Building
    theta_r = LpVariable(f'theta_r')
    lambda_k = LpVariable.dicts(f'lambda_k', lowBound=0, indices=K)
    
    # Objective Function setting
    model += theta_r
    
    # Constraints setting
    for i in I:
        model += lpSum([
                lambda_k[k] * X[i][k]
            for k in K]) <= theta_r * float(X[i][K[r]])
    for j in J:
        model += lpSum([
                lambda_k[k] * Y[j][k]
            for k in K]) >= float(Y[j][K[r]])
    
    # Model solving
    model.solve()
    
    return f'{K[r]}：{round(value(model.objective), 3)}\n', value(model.objective)

def getTechnicalEfficiency(r):

    # Model Building 
    model = LpProblem('VRS_model', LpMinimize) # 建立一個新的model，命名為model
    
    # Decision variables Building 
    theta_r = LpVariable(f'theta_r')
    lambda_k = LpVariable.dicts(f'lambda_k', lowBound=0, indices = K)
    
    # Objective Function setting
    model += theta_r
    
    # Constraints setting
    for i in I:
        model += lpSum([
                lambda_k[k] * X[i][k]
            for k in K]) <= theta_r * float(X[i][K[r]])
    for j in J:
        model += lpSum([
                lambda_k[k] * Y[j][k]
            for k in K]) >= float(Y[j][K[r]])
    model += lpSum([ lambda_k[k] for k in K]) == 1
    
    # model solving 
    model.solve()  
    
    return f'{K[r]}：{round(value(model.objective), 3)}\n', value(model.objective)

scaler = MinMaxScaler()
# Fit scaler to the data and transform it
master_variables[I + J] = scaler.fit_transform(master_variables[I + J])

print(master_variables)

#master_variables[J] = 1 - master_variables[J]
#master_variables[I] = 1 - master_variables[I]

OE_outputText = 'These are OE of all DMUs\n-------------\n'
TE_outputText = 'These are TE of all DMUs\n-------------\n'

for k in range(len(K)):
    OE_text, OE_val = getOverallEfficiency(k)
    TE_text, TE_val = getTechnicalEfficiency(k)
    OE_outputText += OE_text
    TE_outputText += TE_text

print(TE_outputText)


exit()
def get_financial_year(timeperiod):
    if int(timeperiod.split('_')[1]) >= 4:
        return str(int(timeperiod.split('_')[0]))+'-'+str(int(timeperiod.split('_')[0])+1)
    else:
        return str(int(timeperiod.split('_')[0]) - 1)+'-'+str(int(timeperiod.split('_')[0]))
    
# Apply the function to create the 'FinancialYear' column
master_variables['FinancialYear'] = master_variables['timeperiod'].apply(lambda x: get_financial_year(x))


    
#INPUT VARS
government_response_vars = ["total_tender_awarded_value",
                      "SOPD_tenders_awarded_value",
                      "SDRF_tenders_awarded_value",
                      "RIDF_tenders_awarded_value",
                      "LTIF_tenders_awarded_value",
                      "CIDF_tenders_awarded_value",
                      "Preparedness Measures_tenders_awarded_value",
                      "Immediate Measures_tenders_awarded_value",
                      "Others_tenders_awarded_value"
                      ]

# Find cumsum in each FY of the government response vars
for var in government_response_vars:
    master_variables[var]=master_variables.groupby(['object_id','FinancialYear'])[var].cumsum()

#OUTPUT VARS
damage_vars = ["Total_Animal_Affected","Population_affected_Total",
                "Crop_Area","Total_House_Fully_Damaged","Embankments affected",
                 "Roads","Bridge"]

govtresponse_df = master_variables[government_response_vars + damage_vars + ['timeperiod', 'object_id']]


# Function to assign bins based on breaks
def assign_bin(value):
    for i in range(len(breaks)):
        if value <= breaks[i]:
            return i + 1  # Since bins start from 1
    return len(breaks)  # If value is greater than the last break

govtresponse_df_months = []
for month in tqdm(govtresponse_df.timeperiod.unique()[27:28]):
    govtresponse_df_month = govtresponse_df[govtresponse_df.timeperiod == month]
    govtresponse_df_month = govtresponse_df_month.set_index('object_id')
    # Initialize MinMaxScaler
    #scaler = MinMaxScaler()
    # Fit scaler to the data and transform it
    #govtresponse_df_month[damage_vars] = scaler.fit_transform(govtresponse_df_month[damage_vars])

    # Reversing all input vars
    #govtresponse_df_month[government_response_vars] = 1 - govtresponse_df_month[government_response_vars]

    # Reversing all output vars (as more output should be less damage)
    #govtresponse_df_month[damage_vars] = 1 - govtresponse_df_month[damage_vars]

    # Input dict
    X = govtresponse_df_month[government_response_vars].T.to_dict('list')

    # Output dict
    y = govtresponse_df_month[damage_vars].T.to_dict('list')

    DMU = list(govtresponse_df_month.index.astype(int))

    print(y)

    df = DEA.CRS(DMU, X, y, orientation="input", dual=False)


    govtresponse_df_month = govtresponse_df_month.reset_index().merge(df,
                                                          left_on = 'object_id',
                                                          right_on = 'DMU')
    
    # Perform Natural Jenks classification with 5 classes
    try:
        breaks = jenkspy.jenks_breaks(govtresponse_df_month['efficiency'], n_classes=5)
        govtresponse_df_month['government-response'] = pd.cut(govtresponse_df_month['efficiency'],
                                                    bins=breaks,
                                                    labels=[5, 4, 3, 2, 1], #Low efficiency = More Vulnerability
                                                    include_lowest=True)
    except:
        govtresponse_df_month['government-response'] = 5
        print('heh')    
    
    govtresponse_df_months.append(govtresponse_df_month)

govt_response = pd.concat(govtresponse_df_months)

master_variables = master_variables.merge(govt_response[['timeperiod', 'object_id', 'efficiency', 'government-response']],
                       on = ['timeperiod', 'object_id'])

master_variables.to_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1_govtresponse.csv', index=False)



