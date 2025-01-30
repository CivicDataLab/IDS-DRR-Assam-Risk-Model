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
print(os.getcwd())
## INPUT: FACTOR SCORES CSV
factor_scores_dfs = glob.glob(os.getcwd()+r'/RiskScoreModel/data/factor_scores_l1*.csv')

# Select only the columns that exist in both the DataFrame and the list
factors = ['exposure', 'flood-hazard', 'vulnerability', 'government-response']
additional_columns = ['efficiency','flood-hazard-float', 'total_tenders_hist', "SDRF_sanctions_hist", "other_tenders_hist"]

merged_df = pd.read_csv(factor_scores_dfs[0])
print(merged_df.shape)
# Merge successive DataFrames in the list
for df in factor_scores_dfs[1:]:
    df = pd.read_csv(df)
    print(df.shape)
    selected_columns = [col for col in factors if col in df.columns]
    selected_additional_columns = [col for col in additional_columns if col in df.columns]

    # Create a new DataFrame containing only the selected columns
    df = df[selected_columns + ['object_id', 'timeperiod']+selected_additional_columns]
    #merged_df = pd.merge(merged_df, df, on=['object_id', 'timeperiod'], how='inner')
    merged_df = pd.merge(
        merged_df, df, on=['object_id', 'timeperiod'], how='inner', suffixes=('', '_drop')
    )
    # Drop the duplicate columns after the merge
    merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith('_drop')]

#df = pd.read_csv(os.getcwd()+'/RiskScoreModel/data/factor_scores.csv')
'''
#updating govt-response variables to be cumulative
government_response_vars = ["total_tender_awarded_value",
                            "SDRF_sanctions_awarded_value",
                       "SOPD_tenders_awarded_value",
                       "SDRF_tenders_awarded_value",
                       "RIDF_tenders_awarded_value",
                       "LTIF_tenders_awarded_value",
                       "CIDF_tenders_awarded_value",
                       "Preparedness Measures_tenders_awarded_value",
                       "Immediate Measures_tenders_awarded_value",
                       "Others_tenders_awarded_value",
                       
                      ]
govt_response_df = pd.read_csv(r'D:\CivicDataLab_IDS-DRR\IDS-DRR_Github\IDS-DRR-Assam\RiskScoreModel\data\factor_scores_l1_government-response.csv')  # Adjust path
govt_response_df = govt_response_df[['object_id', 'timeperiod'] + government_response_vars]

# Merge govt_response_df into the merged dataframe to update the 'government-response' values
merged_df = pd.merge(merged_df, govt_response_df, on=['object_id', 'timeperiod'], how='left', suffixes=('', '_updated'))

# Update each of the government response variables
for col in government_response_vars:
    merged_df[col] = merged_df[f'{col}_updated']  # Directly replace values with the updated column
    merged_df = merged_df.drop(columns=[f'{col}_updated'])  # Clean up the temporary '_updated' columns
'''
df_months = []

for month in merged_df.timeperiod.unique():

    df_month = merged_df[merged_df.timeperiod==month]

    evaluation_matrix = np.array(df_month[['flood-hazard','exposure','vulnerability','government-response']].values)
    weights = [fldhzd_w,exp_w,vul_w,resp_w]

    criterias = [True, True, True, True]
    # All variables - more is more risk; 'government-response' is in reverse

    t = Topsis(evaluation_matrix, weights, criterias)
    t.calc()
    df_month['TOPSIS_Score'] = t.worst_similarity
    df_month = df_month.sort_values(by='TOPSIS_Score', ascending=False)
    
    compositescorelabels = [1,2,3,4,5]
    compscore = pd.cut(df_month['TOPSIS_Score'],bins = 5,precision = 0,labels = compositescorelabels )
    df_month['risk-score'] = compscore

    df_months.append(df_month)

topsis = pd.concat(df_months)

print(topsis.shape)
topsis.columns = [col.lower().replace('_', '-').replace(' ', '-') for col in topsis.columns]

topsis.to_csv(os.getcwd()+r'/RiskScoreModel/data/risk_score.csv', index=False)

## DISTRICT LEVEL SCORES
dist_ids = pd.read_csv(os.getcwd()+r'/RiskScoreModel/assets/district_objectid.csv')

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


indicators = ['total-tender-awarded-value',
    'sopd-tenders-awarded-value',
    'sdrf-sanctions-awarded-value',
    'sdrf-tenders-awarded-value',
    'ridf-tenders-awarded-value',
    'ltif-tenders-awarded-value',
    'cidf-tenders-awarded-value',
    'preparedness-measures-tenders-awarded-value',
    'immediate-measures-tenders-awarded-value',
    'others-tenders-awarded-value',
    'total-animal-washed-away',
    'total-animal-affected',
    'total-house-fully-damaged',
    'embankments-affected',
    'roads',
    'bridge',
    'embankment-breached',
    'sum-population',
    'inundation-intensity-sum',
    'total-hhd',
    'human-live-lost',
    'sum-aged-population',
    'schools-count',
    'health-centres-count',
    'road-length',
    'rail-length',
    'rc-nosanitation-hhds-pct',
    'drainage-density',
    #'flood-hazard',
    'inundation-pct',
    'inundation-intensity-mean',
    'inundation-intensity-mean-nonzero',
    'avg-electricity',
    'rc-piped-hhds-pct',
    'mean-sex-ratio',
    'population-affected-total',
    'crop-area',
    'elevation-mean',
    'mean-ndvi',
    'mean-ndbi',
    'rc-area',
    #'are-new',
    'riverlevel-mean',
    'riverlevel-min',
    'riverlevel-max',
    'sum-young-population',
    'mean-cn',
    'slope-mean',
    'avg-tele',
    'distance-from-river',
    'water',
    'trees',
    'rangeland',
    'crops',
    'flooded-vegetation',
    'built-area',
    'bare-ground',
    'clouds',
    'net-sown-area-in-hac',
    #'road-count',
    'rail-count',
    'max-rain',
    'mean-rain',
    'sum-rain',
    'efficiency',
    
    #'total-tenders-hist', 
    #"sdrf-sanctions-hist", 
    #"other-tenders-hist",    
    #'flood-hazard-float'

    #'topsis-score',
    #'risk-score',
    #'exposure',
    #'vulnerability',
    #'government-response',
    ]

# Define aggregation rules based on the columns
aggregation_rules = {
    # Sum columns
    'total-tender-awarded-value': 'sum',
    'sopd-tenders-awarded-value': 'sum',
    'sdrf-sanctions-awarded-value': 'sum',
    'sdrf-tenders-awarded-value': 'sum',
    'ridf-tenders-awarded-value': 'sum',
    'ltif-tenders-awarded-value': 'sum',
    'cidf-tenders-awarded-value': 'sum',
    'preparedness-measures-tenders-awarded-value': 'sum',
    'immediate-measures-tenders-awarded-value': 'sum',
    'others-tenders-awarded-value': 'sum',
    'total-animal-washed-away': 'sum',
    'total-animal-affected': 'sum',
    'total-house-fully-damaged': 'sum',
    'embankments-affected': 'sum',
    'roads': 'sum',
    'bridge': 'sum',
    'embankment-breached': 'sum',
    'sum-population': 'sum',
    'inundation-intensity-sum': 'sum',
    'total-hhd': 'sum',
    'human-live-lost': 'sum',
    'sum-aged-population': 'sum',
    'schools-count': 'sum',
    'health-centres-count': 'sum',
    'road-length': 'sum',
    'rail-length': 'sum',
    'sum-rain': 'sum',
    'rc-area':'sum',
    #'are-new':'sum',
    'sum-young-population':'sum',
    'net-sown-area-in-hac':'sum',
    #'road-count':'sum',
    'rail-count':'sum',
    'population-affected-total': 'sum',
    'crop-area': 'sum',

    # Mean for percentage or density-based metrics
    'rc-nosanitation-hhds-pct': 'mean',
    'drainage-density': 'mean',
    #'flood-hazard': 'mean',
    'inundation-pct': 'mean',
    'inundation-intensity-mean-nonzero': 'mean',
    'inundation-intensity-mean': 'mean',
    'avg-electricity': 'mean',
    'rc-piped-hhds-pct': 'mean',
    'mean-sex-ratio': 'mean',
    'mean-rain':'mean',
    'elevation-mean':'mean',
    'mean-ndvi':'mean',
    'mean-ndbi':'mean',
    'riverlevel-mean':'mean',
    'mean-cn':'mean',
    'slope-mean':'mean',
    'avg-tele':'mean',
    'distance-from-river':'mean',
    'water':'mean',
    'trees':'mean',
    'rangeland':'mean',
    'crops':'mean',
    'flooded-vegetation':'mean',
    'built-area':'mean',
    'bare-ground':'mean',
    'clouds':'mean',
    'efficiency':'mean',
    #'total-tenders-hist':'mean', 
    #"sdrf-sanctions-hist":"mean", 
    #"other-tenders-hist":"mean",    
    #'flood-hazard-float':"mean",

    #'topsis-score': 'mean',
    #'risk-score': 'mean',
    #'exposure': 'mean',
    #'vulnerability': 'mean',
    #'government-response': 'mean',

    # Max for hazard levels
    'max-rain':'max',
    'riverlevel-max':'max',
    'riverlevel-min':'min'


}

rounding_rules = {
    'avg-tele': 1,  # Round column 'A' to 1 decimal place
    'avg-electricity': 1,

    'mean-sex-ratio': 2,  
    'inundation-intensity-mean-nonzero': 2,  
    'rc-piped-hhds-pct':2,
    'rc-nosanitation-hhds-pct':2,
    'inundation-intensity-sum':2,
    'max-rain':2,
    'mean-rain':2,
    'sum-rain':2,

    
    'sum-aged-population': 0,   # Round column 'C' to no decimal places
    'sum-young-population': 0,
    'sum-population':0,
    'rail-length':0,
    'road-length':0,
    'elevation-mean':0,
    'slope-mean':0,
    'crop-area':0,

}

dist_indicators = topsis.groupby(['district', 'timeperiod']).agg(aggregation_rules).reset_index()

def apply_rounding_rules(df, rounding_rules):
    """
    Apply multiple rounding rules to a DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    rounding_rules (dict): A dictionary where keys are column names and values are the number of decimals to round to.

    Returns:
    pd.DataFrame: The DataFrame with applied rounding rules.
    """
    for column, decimals in rounding_rules.items():
        if column in df.columns:
            df[column] = df[column].round(decimals)
        else:
            print(f"Column {column} does not exist in DataFrame.")
    return df

'''

dist = pd.concat([dist_indicators, 
                  dist_vul['vulnerability'],
                  dist_exp['exposure'], 
                  dist_govt['government-response'], 
                  dist_haz['flood-hazard'], 
                  dist_risk['risk-score']], 
                  axis=1)
'''
dist = pd.concat([dist_vul.set_index(['district', 'timeperiod']),
                  dist_exp.set_index(['district', 'timeperiod'])['exposure'],
                  dist_govt.set_index(['district', 'timeperiod'])['government-response'],
                  dist_haz.set_index(['district', 'timeperiod'])['flood-hazard'],
                  dist_risk.set_index(['district', 'timeperiod'])['risk-score'],
                  dist_indicators.set_index(['district', 'timeperiod'])[indicators]],
                  axis=1).reset_index()
print(dist.shape)
print(topsis.shape)


final = pd.concat([topsis, dist], ignore_index=True)

# Apply rounding rules
final = apply_rounding_rules(final, rounding_rules)
final['inundation-pct'] = final['inundation-pct']*100


#final = pd.concat([topsis.set_index(['object-id', 'timeperiod']),
#                   dist.set_index(['object-id', 'timeperiod'])], axis=1).reset_index()

final.rename(columns={'preparedness-measures-tenders-awarded-value': 'restoration-measures-tenders-awarded-value', 'mean-sexratio':'sexratio'}, inplace=True)
final.to_csv(os.getcwd()+r'/RiskScoreModel/data/risk_score_final_district.csv', index=False)

#dist.rename(columns={'preparedness-measures-tenders-awarded-value': 'restoration-measures-tenders-awarded-value'}, inplace=True)
#dist.to_csv(os.getcwd()+r'/IDS-DRR-Assam/RiskScoreModel/data/risk_score_final_dist.csv', index=False)

