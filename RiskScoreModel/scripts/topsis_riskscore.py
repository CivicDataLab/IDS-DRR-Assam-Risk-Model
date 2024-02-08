from topsis import Topsis
import pandas as pd
import numpy as np 
import os

fldhzd_w = 4
exp_w = 1
vul_w = 2
resp_w = 2



## MASTER DATA WITH FACTOR SCORES

## INPUT: FACTOR SCORES CSV
df = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores.csv')

df_months = []

for month in df.timeperiod.unique():
    print(month)

    df_month = df[df.timeperiod==month]

    evaluation_matrix = np.array(df_month[[ 'flood-hazard', 'exposure', 'vulnerability','government-response']].values)
    weights = [fldhzd_w,exp_w,vul_w,resp_w]

    criterias = [True, True, True, True]
    # All variables - more is more risk; 'governmetn-response' is in reverse

    t = Topsis(evaluation_matrix, weights, criterias)
    t.calc()
    df_month['TOPSIS_Score'] = t.worst_similarity
    df_month = df_month.sort_values(by='TOPSIS_Score', ascending=False)
    
    compositescorelabels = ['1','2','3','4','5']
    compscore = pd.cut(df_month['TOPSIS_Score'],bins = 5,precision = 0,labels = compositescorelabels )
    df_month['risk-score'] = compscore

    df_months.append(df_month)


topsis = pd.concat(df_months)
topsis.to_csv(os.getcwd()+'/RiskScoreModel/data/risk_score.csv', index=False)
