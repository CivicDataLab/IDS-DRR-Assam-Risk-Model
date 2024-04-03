import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import seaborn as sns
import plotly.express as px
from factor_analyzer import FactorAnalyzer
from factor_analyzer import (ConfirmatoryFactorAnalyzer, ModelSpecificationParser)
import semopy as sem
from semopy import ModelMeans
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import sys

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# The model gives output for each month - selected by the user through a system argument
if len(sys.argv) < 3:
    print("Correct way to run the code: python3 master_datacode_mda.py <YYYY> <MM>")
    exit()
else:
    year_output = str(sys.argv[1])
    month_output = str(sys.argv[2])
    print("Month: ", year_output+"_"+month_output)

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                      STAGE 0&1 : Reading file and creating new variables
# 0. Reading master file
# 0. Using only data after 2021 for modelling as data all on variables is not availabe prior to this
# 1.1 Computing Historic Averages and maximum for Losses and Damages 
# 1.2 Computing Cumulative values for funds allocated in a year - could be modified later
# 1.a Merging data with master file
# 1.4 Defining new variables based on factor analysis: "Flood hazard" - elevation and slope
# 1.5 Defining new variables based on factor analysis: "Vulnerability" - 
# 1.6 Defining new variables based on factor analysis:"Infrastructure" 0
# 1.7 Defining new variables based on factor analysis:"Total Impact"

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# 0. Reading master file
#--------------------

data = pd.read_csv('MASTER_VARIABLES.csv')
data['year'] = data['timeperiod'].str[:4]
data['year'] = data['year'].astype(int)
data['month'] = data['timeperiod'].str[5:]
data['month'] = data['month'].astype(int)

hist_inun_avg = []
hist_inun_max = []
hist_popaff_avg = []
hist_popaff_max = []
hist_cropaff_avg = []
hist_cropaff_max = []
hist_liveslost_max = []
hist_liveslost_avg = []
hist_rcinmate_avg = []
hist_rcinmate_max = []
hist_animaldam_avg = []
hist_animaldam_max = []
hist_landslide_max = []
hist_landslide_avg = []
hist_urbanflood_avg = []
hist_urbanflood_max = []
year = []
RC = []
month = []
cum_total_tender_awarded_value =[]
cum_SOPD_tenders_awarded_value = []
cum_SDRF_tenders_awarded_value = []
cum_RIDF_tenders_awarded_value = []
cum_LTIF_tenders_awarded_value = []
cum_CIDF_tenders_awarded_value = []
cum_Preparedness = []
cum_Immediate = []
cum_Others_tenders_awarded_value = []

rc = data['object_id'].unique()

#1.1 Computing Historic Averages and maximums for Losses and Damages
#----------------------------------------------------
for i in rc:
    for j in range(2021,2024):
        if j == 2021:
            for k in range(5,13):
                month.append(k)
                RC.append(i)
                year.append(j)
                data_index = (data['object_id'] == i)&(data['year'] <= j) &(data['month'] < k)
                data_selected = data[data_index]
                hist_inun_avg.append(data_selected['inundation_pct'].mean())
                hist_inun_max.append(data_selected['inundation_pct'].max())
                hist_animaldam_avg.append(data_selected['Total_Animal_Affected'].mean())
                hist_animaldam_max.append(data_selected['Total_Animal_Affected'].max())
                hist_popaff_avg.append(data_selected['Population_affected_Total'].mean())
                hist_popaff_max.append(data_selected['Population_affected_Total'].max())
                hist_rcinmate_avg.append(data_selected['Relief_Camp_inmates'].mean())
                hist_rcinmate_max.append(data_selected['Relief_Camp_inmates'].max())
                hist_liveslost_avg.append(data_selected['Human_Live_Lost'].mean())
                hist_liveslost_max.append(data_selected['Human_Live_Lost'].max())
                hist_cropaff_avg.append(data_selected['Crop_Area'].mean())
                hist_cropaff_max.append(data_selected['Crop_Area'].max())
        else:
            if j == 2023:
                for k in range(1,9):
                    month.append(k)
                    RC.append(i)
                    year.append(j)
                    data_index = (data['object_id'] == i)&(data['year'] <= j) &(data['month'] < k)
                    data_selected = data[data_index]
                    hist_inun_avg.append(data_selected['inundation_pct'].mean())
                    hist_inun_max.append(data_selected['inundation_pct'].max())
                    hist_animaldam_avg.append(data_selected['Total_Animal_Affected'].mean())
                    hist_animaldam_max.append(data_selected['Total_Animal_Affected'].max())
                    hist_popaff_avg.append(data_selected['Population_affected_Total'].mean())
                    hist_popaff_max.append(data_selected['Population_affected_Total'].max())
                    hist_rcinmate_avg.append(data_selected['Relief_Camp_inmates'].mean())
                    hist_rcinmate_max.append(data_selected['Relief_Camp_inmates'].max())
                    hist_liveslost_avg.append(data_selected['Human_Live_Lost'].mean())
                    hist_liveslost_max.append(data_selected['Human_Live_Lost'].max())
                    hist_cropaff_avg.append(data_selected['Crop_Area'].mean())
                    hist_cropaff_max.append(data_selected['Crop_Area'].max())
            else:
                for k in range(1,13):
                    month.append(k)
                    RC.append(i)
                    year.append(j)
                    data_index = (data['object_id'] == i)&(data['year'] <= j) &(data['month'] < k)
                    data_selected = data[data_index]
                    hist_inun_avg.append(data_selected['inundation_pct'].mean())
                    hist_inun_max.append(data_selected['inundation_pct'].max())
                    hist_animaldam_avg.append(data_selected['Total_Animal_Affected'].mean())
                    hist_animaldam_max.append(data_selected['Total_Animal_Affected'].max())
                    hist_popaff_avg.append(data_selected['Population_affected_Total'].mean())
                    hist_popaff_max.append(data_selected['Population_affected_Total'].max())
                    hist_rcinmate_avg.append(data_selected['Relief_Camp_inmates'].mean())
                    hist_rcinmate_max.append(data_selected['Relief_Camp_inmates'].max())
                    hist_liveslost_avg.append(data_selected['Human_Live_Lost'].mean())
                    hist_liveslost_max.append(data_selected['Human_Live_Lost'].max())
                    hist_cropaff_avg.append(data_selected['Crop_Area'].mean())
                    hist_cropaff_max.append(data_selected['Crop_Area'].max())                  
                    
historic_data = pd.DataFrame(data = RC,columns = ['object_id'])
historic_data['year'] = year
historic_data['month'] = month
historic_data['hist_animaldam_avg'] = hist_animaldam_avg 
historic_data['hist_animaldam_max']  = hist_animaldam_max
historic_data['hist_inun_avg'] = hist_inun_avg
historic_data['hist_inun_max'] = hist_inun_max
historic_data['hist_liveslost_avg'] = hist_liveslost_avg
historic_data['hist_liveslost_max'] = hist_liveslost_max
historic_data['hist_popaff_avg'] = hist_popaff_avg
historic_data['hist_popaff_max'] = hist_popaff_max
historic_data['hist_rcinmate_avg'] = hist_rcinmate_avg
historic_data['hist_rcinmate_max'] = hist_rcinmate_max
historic_data['hist_cropaff_avg'] = hist_cropaff_avg
historic_data['hist_cropaff_max'] = hist_cropaff_max
historic_data.fillna(0,inplace = True)
#historic_data.to_csv('Historic.csv')

RC= []
year = []
month = []

#1.2 Computing Cumulative values for funds allocated in a year
#----------------------------------------------------------
for i in rc:
    for j in range(2021,2024):
        if j == 2021:
            for k in range(5,13):
                month.append(k)
                RC.append(i)
                year.append(j) 
                data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k)
                data_selected = data[data_index]
                cum_CIDF_tenders_awarded_value.append(data_selected['CIDF_tenders_awarded_value'].sum())
                cum_Immediate.append(data_selected['Immediate Measures_tenders_awarded_value'].sum())
                cum_LTIF_tenders_awarded_value.append(data_selected['LTIF_tenders_awarded_value'].sum())
                cum_Others_tenders_awarded_value.append(data_selected['Others_tenders_awarded_value'].sum())
                cum_Preparedness.append(data_selected['Preparedness Measures_tenders_awarded_value'].sum())
                cum_RIDF_tenders_awarded_value.append(data_selected['RIDF_tenders_awarded_value'].sum())
                cum_SDRF_tenders_awarded_value.append(data_selected['SDRF_tenders_awarded_value'].sum())
                cum_SOPD_tenders_awarded_value.append(data_selected['SOPD_tenders_awarded_value'].sum())
                cum_total_tender_awarded_value.append(data_selected['total_tender_awarded_value'].sum())
                
        else:
            if j == 2023:
                for k in range(1,9):
                    month.append(k)
                    RC.append(i)
                    year.append(j) 
                    data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k)
                    data_selected = data[data_index]
                    cum_CIDF_tenders_awarded_value.append(data_selected['CIDF_tenders_awarded_value'].sum())
                    cum_Immediate.append(data_selected['Immediate Measures_tenders_awarded_value'].sum())
                    cum_LTIF_tenders_awarded_value.append(data_selected['LTIF_tenders_awarded_value'].sum())
                    cum_Others_tenders_awarded_value.append(data_selected['Others_tenders_awarded_value'].sum())
                    cum_Preparedness.append(data_selected['Preparedness Measures_tenders_awarded_value'].sum())
                    cum_RIDF_tenders_awarded_value.append(data_selected['RIDF_tenders_awarded_value'].sum())
                    cum_SDRF_tenders_awarded_value.append(data_selected['SDRF_tenders_awarded_value'].sum())
                    cum_SOPD_tenders_awarded_value.append(data_selected['SOPD_tenders_awarded_value'].sum())
                    cum_total_tender_awarded_value.append(data_selected['total_tender_awarded_value'].sum())
            
            else:
                for k in range(1,13):
                    month.append(k)
                    RC.append(i)
                    year.append(j) 
                    data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k)
                    data_selected = data[data_index]
                    cum_CIDF_tenders_awarded_value.append(data_selected['CIDF_tenders_awarded_value'].sum())
                    cum_Immediate.append(data_selected['Immediate Measures_tenders_awarded_value'].sum())
                    cum_LTIF_tenders_awarded_value.append(data_selected['LTIF_tenders_awarded_value'].sum())
                    cum_Others_tenders_awarded_value.append(data_selected['Others_tenders_awarded_value'].sum())
                    cum_Preparedness.append(data_selected['Preparedness Measures_tenders_awarded_value'].sum())
                    cum_RIDF_tenders_awarded_value.append(data_selected['RIDF_tenders_awarded_value'].sum())
                    cum_SDRF_tenders_awarded_value.append(data_selected['SDRF_tenders_awarded_value'].sum())
                    cum_SOPD_tenders_awarded_value.append(data_selected['SOPD_tenders_awarded_value'].sum())
                    cum_total_tender_awarded_value.append(data_selected['total_tender_awarded_value'].sum())
        
cum_tenders = pd.DataFrame(data = RC,columns = ['object_id'])
cum_tenders['year'] = year
cum_tenders['month'] = month
cum_tenders['cum_CIDF_tenders_awarded_value'] = cum_CIDF_tenders_awarded_value
cum_tenders['cum_Immediate'] = cum_Immediate
cum_tenders['cum_LTIF_tenders_awarded_value'] = cum_LTIF_tenders_awarded_value
cum_tenders['cum_Others_tenders_awarded_value'] = cum_Others_tenders_awarded_value
cum_tenders['cum_Preparedness'] = cum_Preparedness
cum_tenders['cum_RIDF_tenders_awarded_value'] = cum_RIDF_tenders_awarded_value
cum_tenders['cum_SDRF_tenders_awarded_value'] = cum_SDRF_tenders_awarded_value
cum_tenders['cum_SOPD_tenders_awarded_value'] = cum_SOPD_tenders_awarded_value
cum_tenders['cum_total_tender_awarded_value'] = cum_total_tender_awarded_value

#1.a Merging data with master file
#----------------------------------
data = data.merge(historic_data,on = ['object_id','year','month'],how = 'left')
data = data.merge(cum_tenders,on = ['object_id','year','month'],how = 'left')
#cum_tenders.to_csv('mergedtenders.csv')

#Sorting data based on object id, year and month
inun_yearsort = data.sort_values(by = ['object_id','year','month']).reset_index(drop = True)
inun_yearsort = inun_yearsort.replace(r'^\s+$', np.nan, regex=True)

#0. Using only data after 2021 for modelling as data all on variables is not availabe prior to this
#-----------------------------------------------------------------------------------------------

dataafter21 = (inun_yearsort['year'] >= 2021) & (inun_yearsort['year'] <= 2023) #2023 could be updated to include present year
inun_yearsort = inun_yearsort[dataafter21]
inun_yearsort.reset_index(drop = True)
#inun_yearsort.to_csv('INUN_landchar.csv')

# 1.3 Computing total area inundated in the revenue circle
# ---------------------------------------------------------
inun_yearsort['inun_area'] = inun_yearsort['rc_area']*inun_yearsort['inundation_pct']
#plt.scatter(inun_yearsort['built_area'],inun_yearsort['total_tender_awarded_value'])
#plt.show()
#plt.close()

data_heads =list( inun_yearsort.columns.values)

# 0. Identify present time period for analysis - Monthly basis
# --------------------------------------------
current_year = (inun_yearsort['year'] == int(year_output)) & (inun_yearsort['month'] == int(month_output)) 
df_all_current = inun_yearsort[current_year]
df_all_curr = pd.DataFrame(data = df_all_current,columns=data_heads)
df_all_curr.reset_index(inplace = True)

scaler = MinMaxScaler()
data_heads.remove('district')
scaler.fit(df_all_curr[data_heads])
data_min_max_scaled = scaler.transform(df_all_curr[data_heads])
df_all_curr_all = pd.DataFrame(data = data_min_max_scaled,columns = data_heads)

#0. Data to be used for modelling and retrieveing coefficients
# -------------------------------------------------------------

#Normalising data
scaler.fit(inun_yearsort[data_heads])
data_min_max_scaled = scaler.transform(inun_yearsort[data_heads])
df_all= pd.DataFrame(data = data_min_max_scaled,columns = data_heads)


# 1.4 Defining new variables based on factor analysis: Flood hazard
#-------------------------------------------------------------------
df_all['floodhazard'] = df_all['elevation_mean'] + df_all['slope_mean']
df_all['waterhazard'] = df_all['mean_cn'] + df_all['water']
df_all['rainfall'] = df_all['max_rain'] + df_all['mean_rain']+df_all['sum_rain']

# 1.5 Defining new variables based on factor analysis: Vulnerability
#-------------------------------------------------------------------
df_all['vulner'] = df_all['rc_piped_hhds_pct']+df_all['avg_electricity']-df_all['rc_nosanitation_hhds_pct']
# Discriminant Analysis with the above variables for three elevations

# 1.6 Defining new variables based on factor analysis:Infrastructure access
#--------------------------------------------------------------------------
df_all['infra'] = df_all['road_length']+df_all['rail_length']+df_all['schools_count']+df_all['health_centres_count']

# 1.7 Defining new variables based on factor analysis:Total Impact
#--------------------------------------------------------------------------
df_all['totalloss'] = df_all['Population_affected_Total']+df_all['Crop_Area']+df_all['Total_Animal_Affected']


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 2: Linear Discriminant Analysis to classify impact
# 2A. Lower elevations (< 50 m ~~ 0.04 scaled and also only monsoon months)
#   2A.1 LDA considering all investigative variables.
#   2A.2 LDA considering only flood hazard variables.
# 2B. Middle elevations (50- 80 ~~ 0.04-0.08)only monsoon months
#   2B.1 LDA using all investigative variables
#   2B.2 Including flood hazard variables
# 2C. High elevations (> 80 m ~~ > 0.08)only monsoon months
#   2C.1 Including all variables of interest
#   2C.2 Including flood hazard variables
# 2D. Population segmented model to determing effect of infrastructure
# 2E. Modelling flood hazard using inundation as dependent variable
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# 2A. Lower elevations
# -.-.-.-.-.-.-.-.-

lowelev = (df_all['elevation_mean'] <= .04) &(df_all['month'] >= .36) &(df_all['month'] <= 0.82)
df_new = pd.DataFrame(data = df_all[lowelev])

# Summative scale based model.
# --------------------------------
print('Summative scale based LDA for low elevation')

#Performing square root transformation to reduce non-normality of data.
#----------------------------------------------------------------------
df_new['totalloss_sqrt'] = np.sqrt(df_new['totalloss'])

# Impact levels are presently chosen as 
# Level 0: Less than or equal to mean
# Level 'n': Mean + ('n-1')*Std. Deviation < X <= Mean + ('n')*Std. Deviation
Impact_level = []
for row in df_new['totalloss_sqrt']:
    if row <= 0.05:
        Impact_level.append(1)
    else:
        if row <= 0.2:
            Impact_level.append(2)
        else:
            if row <= .35:
                Impact_level.append(3)
            else:
                if row <=0.5:
                    Impact_level.append(4) 
                else:
                    if row <=0.65:
                        Impact_level.append(5)
                    else:
                        Impact_level.append(6)
df_new['Impact_level'] = Impact_level

# 2A.1 LDA considering all investigative variables.
# ------------------------------------------
print("All variables")
X = df_new[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
y = df_new['Impact_level']
model2A1 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2A1.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2A1 = np.round(model2A1.coef_,decimals = 3)
intercept2A1 = np.round(model2A1.intercept_,decimals = 3)

print(np.round(params2A1,decimals = 1))
print(np.round(model2A1.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
#    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
#                label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Final model_low elevations')
#display LDA plot
#plt.show()

year_2023 = df_new['year'] == 1
data_2023 = df_new[year_2023]
head_2023 = list(df_new.columns.values)
data_2023 = pd.DataFrame(data = data_2023,columns = head_2023 )


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

train_year = df_new['year'] < 1
train_data = df_new[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
X_test = data_2023[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

# 2A.2 LDA considering only flood hazard variables.
# ------------------------------------------
# Including variables other than factors
print("Flood Hazard variables")
X = df_new[['floodhazard','inun_area','rainfall','distance_from_river']]
y = df_new['Impact_level']
model2A2 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2A2.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2A2 = np.round(model2A2.coef_,decimals = 3)
intercept2A2 = np.round(model2A2.intercept_,decimals = 3)
print(np.round(params2A2,decimals = 1))
print(np.round(model2A2.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
#    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
#                label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Final model_low elevations')
#display LDA plot
#plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

train_year = df_new['year'] < 1
train_data = df_new[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[['floodhazard','inun_area','rainfall','distance_from_river']]
X_test = data_2023[['floodhazard','inun_area','rainfall','distance_from_river']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']
data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

X_train = train_data[['vulner','floodhazard','rainfall','distance_from_river','hist_popaff_max']]
X_test = data_2023[['vulner','floodhazard','rainfall','distance_from_river','hist_popaff_max']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']
data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

# 2B Middle elevations
# ---------------------
midelev = (df_all['elevation_mean'] > .04) & (df_all['elevation_mean'] <= .08) &(df_all['month'] >= .36) &(df_all['month'] <= 0.82)
df_new = pd.DataFrame(data = df_all[midelev])

# Summative scale based model.
print('Summative scale based LDA for middle elevation')

#Performing square root transformation to reduce non-normality of data.
#----------------------------------------------------------------------

df_new['totalloss_sqrt'] = np.sqrt(df_new['totalloss'])
Impact_level = []
for row in df_new['totalloss_sqrt']:
    if row <= 0.05:
        Impact_level.append(1)
    else:
        if row <= 0.2:
            Impact_level.append(2)
        else:
            if row <= .35:
                Impact_level.append(3)
            else:
                if row <=0.5:
                    Impact_level.append(4) 
                else:
                    if row <=0.65:
                        Impact_level.append(5)
                    else:
                        Impact_level.append(6)                
df_new['Impact_level'] = Impact_level

# 2B.1 LDA using all investigative variables
# -------------------------------------------

print('All Variables')
X = df_new[['vulner','floodhazard','inun_area','rainfall','sum_population','distance_from_river','hist_popaff_max']]
y = df_new['Impact_level']
model2B1 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2B1.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2B1 = np.round(model2B1.coef_,decimals = 3)
intercept2B1 = np.round(model2B1.intercept_,decimals = 3)
print(np.round(params2B1,decimals = 1))
print(np.round(model2B1.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
#    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
#                label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Final model_middle elevations')
#display LDA plot
#plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

train_year = df_new['year'] < 1
train_data = df_new[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
X_test = data_2023[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))


X_train = train_data[['vulner','floodhazard','rainfall','distance_from_river','hist_popaff_max']]
X_test = data_2023[['vulner','floodhazard','rainfall','distance_from_river','hist_popaff_max']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

# 2B.2 Including flood hazard variables
#----------------------------------------------
print('Flood Hazard Variables')
X = df_new[['floodhazard','inun_area','rainfall','distance_from_river']]
y = df_new['Impact_level']
model2B2 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2B2.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2B2 = np.round(model2B2.coef_,decimals = 3)
intercept2B2 = np.round(model2B2.intercept_,decimals = 3)
print(np.round(params2B2,decimals = 1))
print(np.round(model2B2.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
#    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
#                label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Final model_middle elevations')
#display LDA plot
#plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

train_year = df_new['year'] < 1
train_data = df_new[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[['floodhazard','inun_area','rainfall','distance_from_river']]
X_test = data_2023[['floodhazard','inun_area','rainfall','distance_from_river']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

# 2C. High Elevations
# ---------------------

highelev = (df_all['elevation_mean'] > .08) &(df_all['month'] >= .36) &(df_all['month'] <= 0.82)
df_new = pd.DataFrame(data = df_all[highelev])

# Summative scale based model.
print('Summative scale based LDA for high elevation')

#Performing square root transformation to reduce non-normality of data.
#----------------------------------------------------------------------
df_new['totalloss_sqrt'] = np.sqrt(df_new['totalloss'])
print(df_new['totalloss_sqrt'].describe())
#print(df_new['Population_affected_Total_sqrt'].describe())

Impact_level = []
for row in df_new['totalloss_sqrt']:
    if row <= 0.05:
        Impact_level.append(1)
    else:
        if row <= 0.2:
            Impact_level.append(2)
        else:
            if row <= .35:
                Impact_level.append(3)
            else:
                if row <=0.5:
                    Impact_level.append(4) 
                else:
                    if row <=0.65:
                        Impact_level.append(5)
                    else:
                        Impact_level.append(6)

df_new['Impact_level'] = Impact_level

# 2C.1 Including all variables of interest
# ----------------------------------------
print('All variables')
X = df_new[['vulner','floodhazard','waterhazard','inun_area','rainfall','cum_Preparedness','distance_from_river','hist_popaff_max']]
y = df_new['Impact_level']
model2C1 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2C1.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2C1 = np.round(model2C1.coef_,decimals = 3)
intercept2C1 = np.round(model2C1.intercept_,decimals = 3)
print(np.round(params2C1,decimals = 0))
print(np.round(model2C1.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
#    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
#                label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Final model_high elevations')
#display LDA plot
#plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

train_year = df_new['year'] < 1
train_data = df_new[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
X_test = data_2023[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

X_train = train_data[['vulner','floodhazard','rainfall','distance_from_river','hist_popaff_max']]
X_test = data_2023[['vulner','floodhazard','rainfall','distance_from_river','hist_popaff_max']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

# 2C.2 Including flood hazard variables
# ---------------------------------------
print('Flood Hazard variables')
X = df_new[['floodhazard','waterhazard','inun_area','rainfall','distance_from_river']]
y = df_new['Impact_level']
model2C2 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2C2.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2C2 = np.round(model2C2.coef_,decimals = 3)
intercept2C2 = np.round(model2C2.intercept_,decimals = 3)
print(np.round(params2C2,decimals = 1))
print(np.round(model2C2.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
#    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
#                label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Final model_high elevations')
#display LDA plot
#plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

train_year = df_new['year'] < 1
train_data = df_new[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[['floodhazard','inun_area','rainfall','distance_from_river']]
X_test = data_2023[['floodhazard','inun_area','rainfall','distance_from_river']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

# 2D. Population segmented model to determe effect of infrastructure 
#-------------------------------------------------------------------
pop_ind = (df_all['sum_population'] <=0.6)& (df_all['sum_population'] > 0.4) &(df_all['month'] >= .36) &(df_all['month'] <= 0.82)
df_pop = df_all[pop_ind]
cols = list(df_all.columns.values)
df_new = pd.DataFrame(data = df_pop,columns = cols)

# Summative scale based model.
print('Summative scale based LDA for equal population')

#Performing square root transformation to reduce non-normality of data.
#----------------------------------------------------------------------
df_new['totalloss_sqrt'] = np.sqrt(df_new['totalloss'])

Impact_level = []
for row in df_new['totalloss_sqrt']:
    if row <= 0.05:
        Impact_level.append(1)
    else:
        if row <= 0.2:
            Impact_level.append(2)
        else:
            if row <= .35:
                Impact_level.append(3)
            else:
                if row <=0.5:
                    Impact_level.append(4) 
                else:
                    if row <=0.65:
                        Impact_level.append(5)
                    else:
                        Impact_level.append(6)
df_new['Impact_level'] = Impact_level

# 2D.1 Including all variables of interest
# -----------------------------------------
print('All variables')
X = df_new[['infra','rainfall']]
y = df_new['Impact_level']
model2D1 = LinearDiscriminantAnalysis(n_components = 2)
data_plot = model2D1.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2D1 = np.round(model2D1.coef_,decimals = 3)
intercept2D1 = np.round(model2D1.intercept_,decimals = 3)
print(np.round(params2D1,decimals = 1))
print(np.round(model2D1.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
#    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
#                label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Final model_population')
#display LDA plot
#plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

train_year = df_new['year'] < 1
train_data = df_new[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
X_test = data_2023[['vulner','floodhazard','inun_area','rainfall','distance_from_river','hist_popaff_max']]
y_train = train_data['Impact_level']
y_test = data_2023['Impact_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

#2E. Modelling Inundation as Flood Hazard
# -----------------------------------------

Inun_level = []
for row in df_all['inundation_pct']:
    if row <= 0.05:
        Inun_level.append(1)
    else:
        if row <= 0.2:
            Inun_level.append(2)
        else:
            if row <= .35:
                Inun_level.append(3)
            else:
                if row <=0.5:
                    Inun_level.append(4) 
                else:
                    if row <=0.75:
                        Inun_level.append(5)
                    else:
                        Inun_level.append(6)

df_all['Inun_level'] = Inun_level
head_2023 = list(df_all.columns.values)
print('Flood Proneness model')
variables = ['floodhazard','rainfall','distance_from_river']
X = df_all[variables]
y = df_all['Inun_level']
model2E1 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2E1.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5','6']
params2E1 = np.round(model2E1.coef_,decimals = 3)
intercept2E1 = np.round(model2E1.intercept_,decimals = 3)
print(np.round(params2E1,decimals = 3))
print(np.round(model2E1.intercept_,decimals = 3))

#creating plot to visualise how grouping is done
#plt.figure()
#colors = [ 'green','lime','yellow','orange','red','black']
#lw = 2
#for color, i, target_name in zip(colors, [1,2,3,4,5,6], target_names):
    #plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
 #               label=target_name)

#add legend to plot
#plt.legend(loc='best', shadow=False, scatterpoints=1)
#plt.title('Summative scale_Inundation Model')
#display LDA plot
#plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 7)
model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

year_2023 = df_all['year'] == 1
data_2023 = df_all[year_2023]
head_2023 = list(df_all.columns.values)
data_2023 = pd.DataFrame(data = data_2023,columns = head_2023 )

train_year = df_all['year'] < 1
train_data = df_all[train_year]
train_data = pd.DataFrame(data = train_data,columns = head_2023)

X_train = train_data[variables]
X_test = data_2023[variables]
y_train = train_data['Inun_level']
y_test = data_2023['Inun_level']

data_plot = model.fit(X_train, y_train).transform(X_train)
y_pred = model.predict(X_test)
#print(y_test)
#print(y_pred)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, y_pred))

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 3: Obtaining factor scores using LDA model of STAGE 2
# 3A. Factor Score: Flood Hazard
# 3B. Factor Score: Exposure
# 3C. Factor Score: Infrastructure Access - should be considered as score for vulnerability
# 3D. Factor Score: Vulnerability - Ignored for present phase
# 3E. Factor Score: Losses and Damages
# 3F. Factor Score: Government Response
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&.
#Dataset: df_all_curr_all (Scaled Data: Min Max Scaler)


# 1.4 Defining new variables based on factor analysis: Flood hazard
#-------------------------------------------------------------------
df_all_curr_all['floodhazard'] = df_all_curr_all['elevation_mean'] + df_all_curr_all['slope_mean']
df_all_curr_all['waterhazard'] = df_all_curr_all['mean_cn'] + df_all_curr_all['water']
df_all_curr_all['rainfall'] = df_all_curr_all['max_rain'] + df_all_curr_all['mean_rain']+df_all_curr_all['sum_rain']

# 1.5 Defining new variables based on factor analysis: Vulnerability
#-------------------------------------------------------------------
df_all_curr_all['vulner'] = df_all_curr_all['rc_piped_hhds_pct']+df_all_curr_all['avg_electricity']-df_all_curr_all['rc_nosanitation_hhds_pct']
# Discriminant Analysis with the above variables for three elevations

# 1.6 Defining new variables based on factor analysis:Infrastructure access
#--------------------------------------------------------------------------
df_all_curr_all['infra'] = df_all_curr_all['road_length']+df_all_curr_all['rail_length']+df_all_curr_all['schools_count']+df_all_curr_all['health_centres_count']

# 1.7 Defining new variables based on factor analysis:Total Impact
#--------------------------------------------------------------------------
df_all_curr_all['totalloss'] = df_all_curr_all['Population_affected_Total']+df_all_curr_all['Crop_Area']+df_all_curr_all['Total_Animal_Affected']

# 3A. Factor Score: Flood Hazard
data_heads = list(df_all_curr_all.columns.values)

#Flood Hazard modelled as Impact
#df_all_curr_all['object_id'] = df_all_curr_all['object_id']*180+101
#Flood Hazard modelled as Flood proneness
object_id = df_all_curr_all['object_id']*180+101
df_all_curr_all['object_id'] = object_id

low = df_all_curr_all['elevation_mean'] <=0.04
lowdata = df_all_curr_all[low]

mid = (df_all_curr_all['elevation_mean'] > .04) & (df_all_curr_all['elevation_mean'] <= .08) 
middata = df_all_curr_all[mid]

high = df_all_curr_all['elevation_mean'] > 0.08
highdata = df_all_curr_all[high]

df_curr_low = pd.DataFrame(data = lowdata,columns = data_heads)
df_curr_mid = pd.DataFrame(data = middata,columns = data_heads)
df_curr_high = pd.DataFrame(data = highdata,columns = data_heads)

X_low = df_curr_low[['floodhazard','inun_area','rainfall','distance_from_river']]
df_curr_low['fldhzrdscore'] = model2A2.predict(X_low)

X_mid = df_curr_mid[['floodhazard','inun_area','rainfall','distance_from_river']]
df_curr_mid['fldhzrdscore'] = model2B2.predict(X_mid)

X_high = df_curr_high[['floodhazard','waterhazard','inun_area','rainfall','distance_from_river']]
df_curr_high['fldhzrdscore'] = model2C2.predict(X_high)

#Weightage
fldhzd_w = 1

#Flood Hazard modelled as Impact
#------------------------------
fldhzrdscore = [df_curr_low,df_curr_mid,df_curr_high]
result = pd.concat(fldhzrdscore)
factorscores = pd.DataFrame(data = result,columns = ['object_id','fldhzrdscore'])

#Flood Hazard modelled as Flood proneness - needs to be investigated for next phase
# ---------------------------------------
#X = df_all_curr_all[variables]
#fldhzrdscore = model2E1.predict(X)
#factorscores = pd.DataFrame(data = object_id,columns = ['object_id'])
#factorscores['fldhzrdscore'] = fldhzrdscore

factorscores = factorscores.sort_values(by = ['object_id']).reset_index(drop = True)
#factorscores['fldhzrdscore'] = factorscores['fldhzrdscore'].astype(int)

# 3B. Factor Score: Exposure
explabels = ['1','2','3','4','5','6']
expscore = pd.cut(df_all_curr_all['sum_population'],bins = 6,precision = 0,labels =explabels )
factorscores['exposurescore'] = expscore
#Weightage
exp_w = 1
#factorscores['exposurescore'] = factorscores['exposurescore'].astype(float)

# 3C. Factor Score: Infrastructure Access : present vulnerability
X = df_all_curr_all[['infra','rainfall']]
infrascore = model2D1.predict(X)
factorscores['infrascore'] = infrascore
#factorscores['infrascore'] = factorscores['infrascore'].astype(float)

#Weightage
sum_w = 0
for i in range(0,len(params2D1)):
    sum_w = sum_w+abs(params2D1[i][0]/params2D1[i][1])
infra_w = sum_w/6

# 3D. Factor Score: Vulnerability : may be ignored
vulnerlabels = ['6','5','4','3','2','1']
vulnerscore = pd.cut(df_all_curr_all['vulner'],bins = 6,precision = 0,labels=vulnerlabels)
#factorscores['vulnerscore'] = vulnerscore
#factorscores['vulnerscore'] = factorscores['vulnerscore'].astype(float)
vul_w = infra_w

# 3E. Factor Score: Losses and Damages
df_all_curr_all['totalloss_sqrt'] = np.sqrt(df_all_curr_all['totalloss'])

Impact_level = []
for row in df_all_curr_all['totalloss_sqrt']:
    if row <= 0.05:
        Impact_level.append(1)
    else:
        if row <= 0.2:
            Impact_level.append(2)
        else:
            if row <= .35:
                Impact_level.append(3)
            else:
                if row <=0.5:
                    Impact_level.append(4) 
                else:
                    if row <=0.65:
                        Impact_level.append(5)
                    else:
                        Impact_level.append(6)
df_all_curr_all['Impact_level'] = Impact_level

hist_impact = []
df_all_curr_all['hist_totalimpact'] = df_all_curr_all['hist_popaff_max']+df_all_curr_all['hist_cropaff_max']+df_all_curr_all['hist_animaldam_max']
df_all_curr_all['histimp_sqrt'] = np.sqrt(df_all_curr_all['hist_totalimpact'])
for row in df_all_curr_all['hist_totalimpact']:
    if row <= df_all_curr_all['hist_totalimpact'].mean():
        hist_impact.append(1)
    else:
        if row <= df_all_curr_all['hist_totalimpact'].mean()+1*df_all_curr_all['hist_totalimpact'].std():
            hist_impact.append(2)
        else:
            if row <= df_all_curr_all['hist_totalimpact'].mean()+2*df_all_curr_all['hist_totalimpact'].std():
                hist_impact.append(3)
            else:
                if row <= df_all_curr_all['hist_totalimpact'].mean()+3*df_all_curr_all['hist_totalimpact'].std():
                    hist_impact.append(4) 
                else:
                    if row <= df_all_curr_all['hist_totalimpact'].mean()+4*df_all_curr_all['hist_totalimpact'].std():
                        hist_impact.append(5)
                    else:
                        hist_impact.append(6)
df_all_curr_all['hist_impact'] = hist_impact
#impactscore = df_all_curr_all[['Impact_level','hist_impact']].max(axis = 1)
impactscore = df_all_curr_all['Impact_level']
factorscores['impact'] = impactscore 
#factorscores['impact'] = factorscores['impact'].astype(float)
imp_w = 1                      

# 3F. Factor Score: Government Response
resplabels = ['6','5','4','3','2','1']
respscore = pd.cut(df_all_curr_all['cum_total_tender_awarded_value'],bins = 6,precision = 0,labels =resplabels )
factorscores['respscore'] = respscore
#factorscores['respscore'] = factorscores['respscore'].astype(float)
resp_w = 1
sum_w = 0
for i in range(0,len(params2C1)):
    sum_w = sum_w+abs(params2C1[i][5]/params2C1[i][4])
resp_w = sum_w/6
print(resp_w)
#factorscores.to_csv('factor.csv')


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 4: TOPSIS for determining composite score
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&.

weights = [fldhzd_w,exp_w,infra_w,imp_w,resp_w]

sum_weights = fldhzd_w+exp_w+infra_w+imp_w+resp_w
weights = weights/sum_weights
print(weights)

topsis_data = factorscores.to_numpy()
#print(topsis_data)
# Computing normalized matrix
for i in range(1,len(weights)+1):
    temp = 0
    for j in range(0,len(topsis_data)):
        temp1 = float(topsis_data[j,i])
        temp = temp + temp1**2
    temp = temp ** 0.5
    
    for j in range(0,len(topsis_data)):
        temp1 = float(topsis_data[j,i])
        topsis_data[j,i] = (temp1/temp)*weights[i-1]


# Calculate ideal best and ideal worst
p_sln = np.min(topsis_data,axis = 0)
n_sln = np.max(topsis_data,axis = 0)

# calculating topsis score
score = [] # Topsis score
pp = [] # distance positive
nn = [] # distance negative
 
 
# Calculating distances and Topsis score for each row
for i in range(len(topsis_data)):
   temp_p, temp_n = 0, 0
   for j in range(1, len(weights)+1):
       temp1 = float(topsis_data[i, j])
       temp_p = temp_p + (p_sln[j] - temp1)**2
       temp_n = temp_n + (n_sln[j] - temp1)**2
   temp_p, temp_n = temp_p**0.5, temp_n**0.5
   score.append(temp_p/(temp_p + temp_n))
   nn.append(temp_n)
   pp.append(temp_p)
   
data_topsis_head = list(factorscores.columns.values)
topsis_data = pd.DataFrame(data = topsis_data,columns = data_topsis_head)
#topsis_data.to_csv('TOPSIS_results_mda.csv')

topsis_data['positive_dist'] = pp
topsis_data['negative_dist'] = nn
topsis_data['Topsis_Score'] = score
print(list(topsis_data.columns.values))
compositescorelabels = ['1','2','3','4','5','6']
compscore = pd.cut(topsis_data['Topsis_Score'],bins = 6,precision = 0,labels = compositescorelabels )
topsis_data['compositescore_grp'] = compscore

# calculating the rank according to topsis score
topsis_data['Rank'] = (topsis_data['Topsis_Score'].rank(method='min', ascending=False))
topsis_data = topsis_data.astype({"Rank": int})
unweighted = ['fldhzrdscore','exposurescore','infrascore','impact','respscore'] 
topsis_data[['fldhzrdscore_un','exposurescore_un','infrascore_un','impact_un','respscore_un']] = factorscores[unweighted]
topsis_data[['elevation_mean','slope_mean','mean_cn','water','inun_area','max_rain','mean_rain','sum_rain','distance_from_river']] = df_all_curr[['elevation_mean','slope_mean','mean_cn','water','inun_area','max_rain','mean_rain','sum_rain','distance_from_river']]
topsis_data['exposurevar'] = df_all_curr['sum_population']
topsis_data[['rail_length','road_length','schools_count','health_centres_count']] = df_all_curr[['rail_length','road_length','schools_count','health_centres_count']]
topsis_data[['Population_affected_Total','Crop_Area','Total_Animal_Affected','hist_popaff_max']] = df_all_curr[['Population_affected_Total','Crop_Area','Total_Animal_Affected','hist_popaff_max']]
topsis_data[['total_tender_awarded_value','cum_Preparedness']] = df_all_curr[['total_tender_awarded_value','cum_Preparedness']]

if int(month_output) <10:
    month_output = '0'+str(month_output)
else:
    month_output = str(month_output)
topsis_data['timeperiod'] = str(year_output)+'_'+str(month_output)
topsis_data['object_id'] = topsis_data['object_id'].apply(lambda x: round(x))
topsis_data.to_csv('LDA/data/TOPSIS_floodproneness_{}_{}.csv'.format(str(year_output), month_output), index=False)
