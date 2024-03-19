from topsis import Topsis
import pandas as pd
import numpy as np 
import os
import glob

fldhzd_w = 4
exp_w = 1
vul_w = 2
resp_w = 2

## MASTER DATA WITH FACTOR SCORES

## INPUT: FACTOR SCORES CSV
factor_scores_dfs = glob.glob(os.getcwd()+'/RiskScoreModel/data/factor_scores_l1*.csv')

# Select only the columns that exist in both the DataFrame and the list
factors = [ 'flood-hazard', 'exposure', 'vulnerability','government-response']


merged_df = pd.read_csv(factor_scores_dfs[0])
# Merge successive DataFrames in the list
for df in factor_scores_dfs[1:]:
    df = pd.read_csv(df)
    selected_columns = [col for col in factors if col in df.columns]
    # Create a new DataFrame containing only the selected columns
    df = df[selected_columns + ['object_id', 'timeperiod']]

    merged_df = pd.merge(merged_df, df, on=['object_id', 'timeperiod'], how='inner')

#df = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores.csv')

df_months = []

for month in merged_df.timeperiod.unique():
    print(month)

    df_month = merged_df[merged_df.timeperiod==month]

    evaluation_matrix = np.array(df_month[[ 'flood-hazard', 'exposure', 'vulnerability','government-response']].values)
    weights = [fldhzd_w,exp_w,vul_w,resp_w]

    criterias = [True, True, True, True]
    # All variables - more is more risk; 'governmetn-response' is in reverse

    t = Topsis(evaluation_matrix, weights, criterias)
    t.calc()
    df_month['TOPSIS_Score'] = t.worst_similarity
    df_month = df_month.sort_values(by='TOPSIS_Score', ascending=False)
    
    compositescorelabels = [1,2,3,4,5]
    compscore = pd.cut(df_month['TOPSIS_Score'],bins = 5,precision = 0,labels = compositescorelabels )
    df_month['risk-score'] = compscore

    df_months.append(df_month)


topsis = pd.concat(df_months)
topsis.columns = [col.lower().replace('_', '-').replace(' ', '-') for col in topsis.columns]
topsis.to_csv(os.getcwd()+'/RiskScoreModel/data/risk_score.csv', index=False)

## DISTRICT LEVEL SCORES
dist_ids = pd.read_csv(os.getcwd()+'/RiskScoreModel/assets/district_objectid.csv')

compositescorelabels = ['1','2','3','4','5']


dist_vul = topsis.groupby(['district','timeperiod'])['vulnerability'].mean().reset_index()
compscore = pd.cut(dist_vul['vulnerability'],bins = 5,precision = 0,labels = compositescorelabels )
dist_vul['vulnerability'] = compscore
dist_vul = dist_vul.merge(dist_ids, on='district')

dist_exp = topsis.groupby(['district','timeperiod'])['exposure'].mean().reset_index()
compscore = pd.cut(dist_exp['exposure'],bins = 5,precision = 0,labels = compositescorelabels )
dist_exp['exposure'] = compscore
dist_exp = dist_exp.merge(dist_ids, on='district')

dist_govt = topsis.groupby(['district','timeperiod'])['government-response'].mean().reset_index()
compscore = pd.cut(dist_govt['government-response'],bins = 5,precision = 0,labels = compositescorelabels )
dist_govt['government-response'] = compscore
dist_govt = dist_govt.merge(dist_ids, on='district')

dist_haz = topsis.groupby(['district','timeperiod'])['flood-hazard'].mean().reset_index()
compscore = pd.cut(dist_haz['flood-hazard'],bins = 5,precision = 0,labels = compositescorelabels )
dist_haz['flood-hazard'] = compscore
dist_haz = dist_haz.merge(dist_ids, on='district')

topsis['risk-score'] = topsis['risk-score'].astype(int)
dist_risk = topsis.groupby(['district','timeperiod'])['risk-score'].mean().reset_index()
compscore = pd.cut(dist_risk['risk-score'],bins = 5,precision = 0,labels = compositescorelabels )
dist_risk['risk-score'] = compscore
dist_risk = dist_risk.merge(dist_ids, on='district')

dist = pd.concat([dist_vul, 
                  dist_exp['exposure'], 
                  dist_govt['government-response'], 
                  dist_haz['flood-hazard'], 
                  dist_risk['risk-score']], 
                  axis=1)

final = pd.concat([topsis, dist], ignore_index=True)
final.rename(columns={'preparedness-measures-tenders-awarded-value': 'restoration-measures-tenders-awarded-value'}, inplace=True)
final.to_csv(os.getcwd()+'/RiskScoreModel/data/risk_score_final.csv', index=False)
