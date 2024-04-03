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
from imblearn.over_sampling import RandomOverSampler # For oversampling and undersampling

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                      STAGE 0&1 : Reading file and creating new variables
# 0. Reading master file
# 0. Using only data after 2021 for modelling as data all on variables is not availabe prior to this
# 1.1 Computing Historic Averages for Losses and Damages 
# 1.2 Computing Cumulative values for funds allocated in a year
# 1.3 Computing Cumulative values for rains as 2 months
# 1.a Merging data with master file
# 1.4 Defining new variables based on factor analysis: Flood hazard
# 1.5 Defining new variables based on factor analysis: Vulnerability
# 1.6 Defining new variables based on factor analysis:Infrastructure access
# 1.7 Defining new variables based on factor analysis:Total Impact
# 1.8 Inundation Analysis
# 1.9 PCA for land clusters
# 1.10 Rainfall Characteristic
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Oversampling and Undersampling techniques
# 

#defining oversampling strategy
# ------------------------------
oversampler = RandomOverSampler(random_state = 0)

#USER INPUTS
# ---------

present_month = 6
present_year = 2022
# 0. Reading master file
#--------------------

data = pd.read_csv('MASTER_VARIABLES.csv')
data = data[(data['year']<=present_year)]

districtrc = pd.read_csv('DistrictRC.csv')

hist_inun_avg = []
hist_inun_max = []
hist_inun1_avg = []
hist_inun1_max = []
hist_inun2_avg = []
hist_inun2_max = []
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
hist_housedam_max = []
hist_housedam_avg = []
hist_roads_avg = []
hist_roads_max = []
hist_bridge_avg = []
hist_bridge_max = []
hist_embank_avg = []
hist_embank_max = []
hist_maxrain = []
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
cum_sum_rain_2mnth = []
cum_max_rain_2mnth = []
cum_mean_rain_2mnth = []
previous_cum_sum = []
previous_cum_max = []
previous_cum_mean = []
previous_sum = []
previous_mean = []
previous_max = []
previous_sum.append(0)
previous_cum_sum.append(0)
previous_cum_max.append(0)
previous_max.append(0)
previous_cum_mean.append(0)
previous_mean.append(0)

rc = data['object_id'].unique()

#0.1 Creating timeline id
# ------------------------

p = 0

conditions = [(data['year'] == 2021)&(data['month'] == 4),
(data['year'] == 2021)&(data['month'] == 5),(data['year'] == 2021)&(data['month'] == 6),
(data['year'] == 2021)&(data['month'] == 7),(data['year'] == 2021)&(data['month'] == 8),
(data['year'] == 2021)&(data['month'] == 9),(data['year'] == 2021)&(data['month'] == 10),
(data['year'] == 2021)&(data['month'] == 11),(data['year'] == 2021)&(data['month'] == 12),
(data['year'] == 2022)&(data['month'] == 1),(data['year'] == 2022)&(data['month'] == 2),
(data['year'] == 2022)&(data['month'] == 3),(data['year'] == 2022)&(data['month'] == 4),
(data['year'] == 2022)&(data['month'] == 5),(data['year'] == 2022)&(data['month'] == 6),
(data['year'] == 2022)&(data['month'] == 7),(data['year'] == 2022)&(data['month'] == 8),
(data['year'] == 2022)&(data['month'] == 9),(data['year'] == 2022)&(data['month'] == 10),
(data['year'] == 2022)&(data['month'] == 11),(data['year'] == 2022)&(data['month'] == 12),
(data['year'] == 2023)&(data['month'] == 1),(data['year'] == 2023)&(data['month'] == 2),
(data['year'] == 2023)&(data['month'] == 3),(data['year'] == 2023)&(data['month'] == 4),
(data['year'] == 2023)&(data['month'] == 5),(data['year'] == 2023)&(data['month'] == 6),
(data['year'] == 2023)&(data['month'] == 7),(data['year'] == 2023)&(data['month'] == 8)
]

values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

data['time_stamp'] = np.select(conditions,values)

#1.1 Computing Historic Averages for Losses and Damages
#----------------------------------------------------
for i in rc:
    for k in range(1,30):
        month.append(k)
        RC.append(i)
        data_index = (data['object_id'] == i) & (data['time_stamp'] < k)
        data_selected = data[data_index]
        hist_inun_avg.append(data_selected['inundation_pct'].mean())
        hist_inun_max.append(data_selected['inundation_pct'].max())
        hist_inun1_avg.append(data_selected['inundation_intensity_mean_nonzero'].mean())
        hist_inun1_max.append(data_selected['inundation_intensity_mean_nonzero'].max())
        hist_inun2_avg.append(data_selected['inundation_intensity_sum'].mean())
        hist_inun2_max.append(data_selected['inundation_intensity_sum'].max())
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
        hist_bridge_avg.append(data_selected['Bridge'].mean())
        hist_bridge_max.append(data_selected['Bridge'].max())
        hist_embank_avg.append(data_selected['Embankment breached'].mean())
        hist_embank_max.append(data_selected['Embankment breached'].max())
        hist_housedam_avg.append(data_selected['Total_House_Fully_Damaged'].mean())
        hist_housedam_max.append(data_selected['Total_House_Fully_Damaged'].max())
        hist_roads_avg.append(data_selected['Roads'].mean())
        hist_roads_max.append(data_selected['Roads'].max())
        hist_maxrain.append(data_selected['max_rain'].max())
                                              
historic_data = pd.DataFrame(data = RC,columns = ['object_id'])
historic_data['time_stamp'] = month
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
historic_data['hist_bridge_avg'] = hist_bridge_avg
historic_data['hist_bridge_max'] = hist_bridge_max
historic_data['hist_embank_avg'] = hist_embank_avg
historic_data['hist_embank_max'] = hist_embank_max
historic_data['hist_housedam_avg'] = hist_housedam_avg
historic_data['hist_housedam_max'] = hist_housedam_max
historic_data['hist_roads_avg'] = hist_roads_avg
historic_data['hist_roads_max'] = hist_roads_max
historic_data['hist_inun1_avg'] = hist_inun1_avg
historic_data['hist_inun1_max'] = hist_inun1_max
historic_data['hist_inun2_avg'] = hist_inun2_avg
historic_data['hist_inun2_max'] = hist_inun2_max
historic_data['hist_maxrain'] = hist_maxrain

historic_data.fillna(0,inplace = True)
historic_data.to_csv('Historic.csv')

RC= []
year = []
month = []

#1.2 Computing Cumulative values for funds allocated in a year
#----------------------------------------------------------
for i in rc:
    for j in range(2021,present_year+1):
        if j == 2021:
            for k in range(4,13):
                month.append(k)
                RC.append(i)
                year.append(j) 
                data_index = (data['object_id'] == i) &(data['time_stamp'] <= k-3)
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
                    if (k<= 3):
                        data_index = (data['object_id'] == i) & (data['time_stamp'] >= 13) & (data['time_stamp'] <= 22 + k)
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
                    if (k > 3):
                        data_index = (data['object_id'] == i) & (data['time_stamp'] >= 26) & (data['time_stamp'] <= 22 + k)
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
                    if k <= 3:
                        data_index = (data['object_id'] == i) & (data['time_stamp'] >= 10) & (data['time_stamp'] <= 9 + k)
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
                    if k > 3:
                        data_index = (data['object_id'] == i) & (data['time_stamp'] >= 13) & (data['time_stamp'] <= 9 + k)
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

RC= []
year = []
month = []

#1.3 Computing Cumulative values for rainfall - 3 month and 2 month cumulatives
#-------------------------------------------------------------------------------
for i in rc:
    for j in range(2021,2024):
        if j == 2021:
            for k in range(4,13):
                month.append(k)
                RC.append(i)
                year.append(j) 
                if k == 4:
                    data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k)
                    
                else:
                    if k == 5:
                        data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k) & (data['month'] > k-1)
                    else:
                        data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k) & (data['month'] > k-2)
                    
                data_selected = data[data_index]
                cum_sum_rain_2mnth.append(data_selected['sum_rain'].sum())
                cum_max_rain_2mnth.append(data_selected['max_rain'].max())
                cum_mean_rain_2mnth.append(data_selected['mean_rain'].mean())
                previous_cum_max.append(data_selected['sum_rain'].max())
                previous_cum_mean.append(data_selected['max_rain'].mean())
                previous_cum_sum.append(data_selected['mean_rain'].sum())
                                               
        else:
            if j == 2023:
                for k in range(1,9):
                    month.append(k)
                    RC.append(i)
                    year.append(j) 
                    if k == 1:
                        data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k)
                    else:
                        if k == 2:
                            data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k) & (data['month'] > k-1)
                        else:
                            data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k) & (data['month'] > k-2)
                    data_selected = data[data_index]
                    cum_sum_rain_2mnth.append(data_selected['sum_rain'].sum())
                    cum_max_rain_2mnth.append(data_selected['max_rain'].max())
                    cum_mean_rain_2mnth.append(data_selected['mean_rain'].mean())
                    previous_cum_max.append(data_selected['sum_rain'].max())
                    previous_cum_mean.append(data_selected['max_rain'].mean())
                    previous_cum_sum.append(data_selected['mean_rain'].sum())            
            else:
                for k in range(1,13):
                    month.append(k)
                    RC.append(i)
                    year.append(j) 
                    if k == 1:
                        data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k)
                    else:
                        if k == 2:
                            data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k) & (data['month'] > k-1)
                        else:
                            data_index = (data['object_id'] == i) & (data['year'] == j ) &(data['month'] <= k) & (data['month'] > k-2)
                    data_selected = data[data_index]
                    cum_sum_rain_2mnth.append(data_selected['sum_rain'].sum())
                    cum_max_rain_2mnth.append(data_selected['max_rain'].max())
                    cum_mean_rain_2mnth.append(data_selected['mean_rain'].mean())
                    previous_cum_max.append(data_selected['sum_rain'].max())
                    previous_cum_mean.append(data_selected['max_rain'].mean())
                    previous_cum_sum.append(data_selected['mean_rain'].sum())

previous_cum_max.pop()
previous_cum_mean.pop()
previous_cum_sum.pop()

cum_rain = pd.DataFrame(data = RC,columns = ['object_id'])
cum_rain['year'] = year
cum_rain['month'] = month
cum_rain['cum_sum_rain_2mnth'] = cum_sum_rain_2mnth
cum_rain['cum_max_rain_2mnth'] = cum_max_rain_2mnth
cum_rain['cum_mean_rain_2mnth'] = cum_mean_rain_2mnth
cum_rain['previous_cum_max'] = previous_cum_max
cum_rain['previous_cum_mean'] = previous_cum_mean
cum_rain['previous_cum_sum'] = previous_cum_sum

#1.a Merging data with master file
#----------------------------------
data = data.merge(historic_data,on = ['object_id','time_stamp'],how = 'left')
data = data.merge(cum_tenders,on = ['object_id','year','month'],how = 'left')
data = data.merge(cum_rain,on = ['object_id','year','month'],how = 'left')
data = data.merge(districtrc[['object_id','District']],on = ['object_id'],how = 'left')
cum_tenders.to_csv('mergedtenders.csv')
cum_rain.to_csv('2monthcumulativerain.csv')

#Sorting data based on object id, year and month
inun_yearsort = data.sort_values(by = ['object_id','year','month']).reset_index(drop = True)
inun_yearsort = inun_yearsort.replace(r'^\s+$', np.nan, regex=True)
#0. Using only data after 2021 for modelling as data all on variables is not availabe prior to this
#-----------------------------------------------------------------------------------------------

dataafter21 = (inun_yearsort['year'] >= 2021) & (inun_yearsort['year'] <= present_year) #2023 could be updated to include present year
inun_yearsort = inun_yearsort[dataafter21]
inun_yearsort.reset_index(drop = True)
inun_yearsort.to_csv('INUN_landchar.csv')

# Computing total area inundated in the revenue circle
# ---------------------------------------------------------
inun_yearsort['inun_area'] = inun_yearsort['rc_area']*inun_yearsort['inundation_pct']
#plt.scatter(inun_yearsort['built_area'],inun_yearsort['total_tender_awarded_value'])
#plt.show()
#plt.close()

data_heads =list( inun_yearsort.columns.values)

#0. Data to be used for modelling and retrieveing coefficients
# -------------------------------------------------------------

#Normalising data
scaler = MinMaxScaler()
data_heads.remove('district')
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
df_all['phyvulner'] = df_all['rc_piped_hhds_pct']+df_all['avg_electricity']-df_all['rc_nosanitation_hhds_pct']

# 1.6 Defining new variables based on factor analysis:Infrastructure access
#--------------------------------------------------------------------------
df_all['infravulner'] = df_all['road_length']+df_all['rail_length']+df_all['schools_count']+df_all['health_centres_count'] - df_all['Embankment breached'] 

# 1.7 Defining new variables based on factor analysis:Total Impact
#--------------------------------------------------------------------------
df_all['totalloss'] = df_all['Population_affected_Total']+df_all['Crop_Area']+df_all['Total_Animal_Affected']

df_all['totalexposure'] = df_all['sum_population']+df_all['total_hhd']

# 1.8 Inundation Analysis
# --------------------------

# Considering EFA grouped the following variables together, namely:
        # 1a. Elevation
        # 1b. Slope
        # 1c. Drainage Density
        # 1d. Trees
        # 1e. Crops
        # 2a. Water
        # 2b. Mean_cn
        # 2c. Rangeland
      

inunmths = (inun_yearsort['month'] >=5 )&(inun_yearsort['month']<=9)

df_inun = df_all[inunmths.reset_index(drop=True)]
inunyearsort_inun = inun_yearsort[inunmths]
print(df_inun['inundation_intensity_sum'].describe())
print(inunyearsort_inun['inundation_intensity_sum'].describe())
#plt.hist(df_inun['Inun_level'],bins = 5)

##########################################################################################################
# 1.9 PCA for Land characteristics and Clustering Revenue Circles on that basis
#---------------------------------------------------------------------------------

pca = PCA(n_components=2)

fldhzrd = ['elevation_mean','slope_mean','drainage_density','trees','water','built_area',
'bare_ground','rangeland','mean_cn','distance_from_river','crops']
df_all_1 = df_all[['object_id','elevation_mean','slope_mean','drainage_density','trees',
'water','built_area','bare_ground','rangeland','mean_cn','distance_from_river','crops']]
print('PCA Analysis for fldhzrd:')
pca_df_fld = pca.fit_transform(df_all_1[fldhzrd])
print(pca.explained_variance_ratio_)
#print(pca_df_fld)
scores = pca_df_fld
#print(scores)
loadings = pca.components_
txt = []
txt = df_all_1['object_id']
fig, ax = plt.subplots()
# Annotate with revenue circle ID
#j = 0
#for i in txt:
#    ax.annotate(i,(scores[j,0],scores[j,1]))
#    j = j+1
    
# Plot the loadings
for i, v in enumerate(loadings.T):
    ax.arrow(0, 0, v[0], v[1], head_width=0.1, head_length=0.1)
    ax.text(v[0] * 1.1, v[1] * 1.1, fldhzrd[i])

# Set the axis limits
#ax.set_xlim(-1, 1)
#ax.set_ylim(-1, 1)

# Set the axis labels
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
plt.title('Clustering using PCA of Land Characteristics')

# K means cluster
pca_df_fld_2 = pca_df_fld[:,[0,1]]


#Find optimum number of cluster
#sse = [] #SUM OF SQUARED ERROR
#for k in range(1,11):
#    km = KMeans(n_clusters=k, random_state=2)
#    km.fit(pca_df_fld_2)
 #   sse.append(km.inertia_)


#sns.set_style("whitegrid")
#g=sns.lineplot(x=range(1,11), y=sse)
 
#g.set(xlabel ="Number of cluster (k)",
 #     ylabel = "Sum Squared Error",
  #    title ='Elbow Method')
 
#plt.show()

Kmean = KMeans(n_clusters = 8)
Kmean.fit(pca_df_fld_2)

pred = Kmean.fit_predict(pca_df_fld_2)
kcls = Kmean.cluster_centers_
print(kcls)
arr = kcls[np.argsort(kcls[:,0])]
print(arr)

rate_8 = np.where(kcls[:,0] == arr[0][0])[0][0]
print("rate_8 cluster:  ",rate_8)
rate_7 = np.where(kcls[:,0] == arr[1][0])[0][0]
print("rate_7 cluster: ",rate_7)
rate_6 = np.where(kcls[:,0] == arr[2][0])[0][0]
print("rate_6 cluster:  ",rate_6)
rate_5 = np.where(kcls[:,0] == arr[3][0])[0][0]
print("rate_5 cluster: ",rate_5)
rate_4 = np.where(kcls[:,0] == arr[4][0])[0][0]
print("rate_4 cluster:  ",rate_4)
rate_3 = np.where(kcls[:,0] == arr[5][0])[0][0]
print("rate_3 cluster:  ",rate_3)
rate_2 = np.where(kcls[:,0] == arr[6][0])[0][0]
print("rate_2 cluster:  ",rate_2)
rate_1 = np.where(kcls[:,0] == arr[7][0])[0][0]
print("rate_1 cluster:  ",rate_1)


#print(type(pred))# Plot the scores

pred_all = pd.DataFrame(data = df_all_1['object_id'],columns=['object_id'])
pred_all['Fldhzrd'] = pred
safety_rate = []
for i in range(0,len(pred)):
    if pred[i] == rate_1:
        safety_rate.append(1)
    else:
        if pred[i] == rate_2:
            safety_rate.append(2)
        else:
            if pred[i] == rate_3:
                safety_rate.append(3)
            else:
                if pred[i] == rate_4:
                    safety_rate.append(4)
                else:
                    if pred[i] == rate_5:
                        safety_rate.append(5)
                    else:
                        if pred[i] == rate_6:
                            safety_rate.append(6)    
                        else:
                            if pred[i] == rate_7:
                                safety_rate.append(7)
                            else:
                                if pred[i] == rate_8:
                                    safety_rate.append(8)

print(len(safety_rate))   
pred_all['fldhzrd_safety_rank'] = safety_rate
pred_all.to_csv('physicalchar.csv')
ax.scatter(scores[:, 0], scores[:, 1],c=pred,cmap = cm.Accent)

#ax.scatter(pca_df_fld_2[ : , 0], pca_df_fld_2[ : , 1])
i = 8
for center in arr: 
    center = center[:2]
    plt.scatter(center[0],center[1],marker = '^',c = 'red',s = 30)
    plt.text(center[0]+0.05,center[1],i, horizontalalignment='left', size='medium', color='black')
    i = i-1

plt.savefig('physicalchar_1.png')
Kmean.labels_

# Save the plot
plt.savefig('physical cluster', bbox_inches='tight')
plt.close()

############################################################################################################
df_all['fldhzrd_safety_rank'] = pred_all['fldhzrd_safety_rank']

Inun_level = []
for row in df_all['inundation_intensity_sum']:
    if row <= df_inun['inundation_intensity_sum'].quantile(0.1):
        Inun_level.append(1)
    else:
        if row <= df_inun['inundation_intensity_sum'].mean()+df_inun['inundation_intensity_sum'].std():
            Inun_level.append(2)
        else:
            if row <= df_inun['inundation_intensity_sum'].mean()+2*df_inun['inundation_intensity_sum'].std():
                Inun_level.append(3)
            else:
                if row <= df_inun['inundation_intensity_sum'].mean()+ 3* df_inun['inundation_intensity_sum'].std():
                    Inun_level.append(4) 
                else:
                    Inun_level.append(5)
 
df_all['Inun_level'] = Inun_level
############################################################################################################
rc = df_all['object_id'].unique()
inun1 = []
inun2 = []
inun3 = []
inun4 = []
inun5 = []

for i in rc:
    df_cluster1 = df_all[(df_all['object_id']== i)&(df_all['month']>=0.33)&(df_all['month']<=0.7)]
    inunlist = list(df_cluster1['Inun_level'])
    inun1.append(inunlist.count(1))
    inun2.append(inunlist.count(2))
    inun3.append(inunlist.count(3))
    inun4.append(inunlist.count(4))
    inun5.append(inunlist.count(5))

rc_inundata = pd.DataFrame(data = rc,columns = ['object_id'])
rc_inundata['Inun1'] = inun1
rc_inundata['Inun2'] = inun2
rc_inundata['Inun3'] = inun3
rc_inundata['Inun4'] = inun4
rc_inundata['Inun5'] = inun5

df_all = df_all.merge(rc_inundata,on=['object_id'],how = 'left')
df_all_low = df_all[(df_all['Inun1'] == 12)]

plt.boxplot(df_inun['inundation_intensity_sum'])
plt.title('Inundation intensity')
plt.savefig('Boxplot for inundation intensity.png')
plt.close()
#############################################################################################################

# 1.10 Rainfall characteristics
# ------------------------------

print(df_all['sum_rain'].describe())

plt.boxplot(df_all['sum_rain'])
plt.title('Sum rain')
plt.savefig('Boxplot for rain.png')
plt.close()


rain_level = []
for row in df_all['sum_rain']:
    if row <= df_all['sum_rain'].mean():
        rain_level.append(1)
    else:
        if row <= df_all['sum_rain'].mean()+1*df_all['sum_rain'].std():
            rain_level.append(2)
        else:
            if row <= df_all['sum_rain'].mean()+2*df_all['sum_rain'].std():
                rain_level.append(3)
            else:
                if row <= df_all['sum_rain'].mean()+3*df_all['sum_rain'].std():
                    rain_level.append(4) 
                else:
                    rain_level.append(5)
 
df_all['rain_level'] = rain_level
rain1 = []
rain2 = []
rain3 = []
rain4 = []
rain5 = []

for i in rc:
    df_cluster1 = df_all[(df_all['object_id']== i)&(df_all['month']>=0.33)&(df_all['month']<=0.7)]
    rainlist = list(df_cluster1['rain_level'])
    rain1.append(rainlist.count(1))
    rain2.append(rainlist.count(2))
    rain3.append(rainlist.count(3))
    rain4.append(rainlist.count(4))
    rain5.append(rainlist.count(5))
    
rc_raindata = pd.DataFrame(data = rc,columns=['object_id'])
rc_raindata['rain1'] = rain1
rc_raindata['rain2'] = rain2
rc_raindata['rain3'] = rain3
rc_raindata['rain4'] = rain4
rc_raindata['rain5'] = rain5


df_all = df_all.merge(rc_raindata,on=['object_id'],how = 'left')

#for i in rc:
#    df_cluster1 = df_all[(df_all['object_id'] == i)&(df_all['month']>=0.33)&(df_all['month']<=0.7)]
#    plt.hist(df_cluster1['rain_level'],bins=[1,2,3,4,5,6],color = 'skyblue', edgecolor='black',density = True)
#    j = int(i*180+101)
#    plt.title('Rain levels for revenu circle '+str(j))
#    plt.xlabel('Rain Level')
#    plt.ylabel('Frequency')
#    plt.savefig('rain level '+str(j)+'.png')
#    plt.close()

# Score Matrix
# ------------

revenuecircles = inun_yearsort['object_id'].unique()

score = pd.DataFrame(data = revenuecircles, columns = ['object_id'])
score = score.merge(districtrc[['object_id','District']],on = ['object_id'],how = 'left')
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 2: Obtaining factor scores using LDA model of STAGE 2
# 2A. Factor Score: Flood Hazard
# 2B. Factor Score: Exposure
# 2C. Factor Score: Vulnerability 
# 2D. Factor Score: Government Response
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&.

# 2A. Flood Hazard Score
# ----------------------

#Flood Hazard Score has 4 components:
# 1. Present Inundation Intensity with 50% weightage
# 2. Expected Inundation for present month's rainfall with 20% weightage
# 3. Historic Inundation with only 5% chance of being exceeded with 15% weightage
# 4. Physical Characteristic of land based inundation with 5% chance of being exceeded and 15% weightage

total_fldscore = []
present_fldscore = []
present_rain = []
rainfall_fldscore = []
historic_fldscore = []
physical_fldscore = []
hist_90percentile_inun = []
phy_cluster = []
cluster_rc = []
rain_db_rc = []
rain_db_rain = []
rain_db_inunmax = []

# 2A.1 Database with frequency Analysis
# ------------------------------------

for i in range(1,9):
    df_cluster1  = df_all[(df_all['fldhzrd_safety_rank'] == i)]
    phy_cluster.append(round(df_cluster1['Inun_level'].quantile(0.95)))
    

for i in rc:
    rc_data = df_all[df_all['object_id'] == i]
    hist_90percentile_inun.append(round(rc_data['Inun_level'].quantile(0.95)))
    cluster_rc.append(rc_data['fldhzrd_safety_rank'].mean())
# Creating database with columns: revenue circle id, rain level, max inundation observed for the rainfall level
for i in rc:
    rc_data = df_all[(df_all['object_id'] == i)]
    j = 1
    while j<= 5:
        raindb = rc_data[(rc_data['rain_level'] == j)]
        rain_db_rc.append(i)
        rain_db_rain.append(j)
        if len(raindb) == 0:
            inunvalue = round(rc_data['Inun_level'].mean())
        else:
            inunvalue = round(raindb['Inun_level'].quantile(0.95))
        rain_db_inunmax.append(inunvalue)
        j = j+1

rain_inun_db = pd.DataFrame(data = rain_db_rc,columns = ['object_id'])
rain_inun_db['rain_db_rain'] = rain_db_rain
rain_inun_db['rain_db_inunmax'] = rain_db_inunmax
rain_inun_db.to_csv('rain_inun_db.csv')

# 2A.1.1 Computing the flood hazard scores
# ------------------------------------
if present_year == 2021:
    max_year_scaled = 0
else:
    max_year_scaled = 1
present_data_index = (df_all['year'] == max_year_scaled) & (round(df_all['month']*11+1) == present_month)
present_data = df_all[present_data_index]
present_data.to_csv('present_data.csv')
j = 0
for i in rc:
    data_interest = present_data[(present_data['object_id'] == i)]
    present_fldscore.append(data_interest['Inun_level'].iloc[0])
    present_rain.append(data_interest['rain_level'].iloc[0])
    rainnow = int(data_interest['rain_level'].iloc[0])
    historic_fldscore.append(hist_90percentile_inun[j])
    physical_fldscore.append(phy_cluster[int(cluster_rc[j])-1])
    rainfall_fldscore.append(rain_inun_db[((rain_inun_db['object_id']) == i) & (rain_inun_db['rain_db_rain'] == rainnow)].rain_db_inunmax.iloc[0])
    j = j+1

# 2A.1.2 Writing to file
# ------------------------------------
score['present_fldscore'] = present_fldscore
score['historic_fldscore'] = historic_fldscore
score['physical_fldscore'] = physical_fldscore
score['present_rain'] = present_rain
score['rainfall_fldscore'] = rainfall_fldscore
score['flood_hazard_score'] = round(0.5*score['present_fldscore']+.2*score['rainfall_fldscore']+0.15*score['physical_fldscore']+0.15*score['historic_fldscore'])

#Weightage
fldhzd_w = 2

# 2B. Exposure Score
# ------------------

expscore = []
for row in present_data['totalexposure']:
    if row <= present_data['totalexposure'].mean():
        expscore.append(1)
    else:
        if row <= present_data['totalexposure'].mean()+present_data['totalexposure'].std():
            expscore.append(2)
        else:
            if row <= present_data['totalexposure'].mean()+2*present_data['totalexposure'].std():
                expscore.append(3)
            else:
                if row <= present_data['totalexposure'].mean()+3*present_data['totalexposure'].std():
                    expscore.append(4) 
                else:
                    expscore.append(5)

score['exposurescore'] = expscore
#Weightage
exp_w = 1
#factorscores['exposurescore'] = factorscores['exposurescore'].astype(float) 

# 2C. Vulnerability Score
# -----------------------
# Variables under vulnerability include:
# Socio - economic Vulnerability
# ..............................
# 1. crops  - not included
# 2. sum_aged_population
# 3. sum_young_population
# 4. mean_sexratio
# Infrastructure (infra)
# ..............
# 5. schools_count
# 6. health_centres_count
# 7. rail_length
# 8. road_length
# Physical systems (vulner)
# .................
# 9. net_sown_area_in_hac
# 10. avg_electricity
# 11. avg_telephone
# 12. rc_piped_hhds_pct
# 13. rc_nosanitation_hhds_pct
# Damages and Losses: Production System
# ...............................
# 14. Total_Animal_Washed_Away
# 15. Total_Animal_Affected
# 16. Crop area
# Damages and Losses: Physical Infrastructure
# ...........................................
# 17. Total_House_Fully_Damaged
# 18. Embankments affected
# 19. Roads
# 20. Bridge
# 21. Embankment breached
# Socio-economic
#...............
# 22. Population_affected_Total
# 23. Relief_Camp_inmates
# 24. Human_Live_Lost
# 25. Number Relief camps


df_all['sociovulner'] = df_all['net_sown_area_in_hac']+df_all['sum_aged_population']+df_all['sum_young_population']+df_all['mean_sexratio']

# Already defined in 1.6
#-----------------------
# df_all['infravulner'] = df_all['road_length']+df_all['rail_length']+df_all['schools_count']+df_all['health_centres_count']

# Already defined in 1.5 
#------------------------
# df_all['phyvulner'] = df_all['rc_piped_hhds_pct']+df_all['avg_electricity']-df_all['rc_nosanitation_hhds_pct']


# Redefining Total loss
# ---------------------
df_all['prodsysloss'] = df_all['Total_Animal_Affected']+df_all['Total_Animal_Washed_Away']+df_all['Crop_Area']
df_all['infraloss'] = df_all['Total_House_Fully_Damaged']+df_all['Embankments affected']+df_all['Roads']+df_all['Bridge']
df_all['socloss'] = df_all['Population_affected_Total']
df_all['totalloss'] = 0.4*df_all['prodsysloss']+0.2*df_all['infraloss']+0.4*df_all['Population_affected_Total']

inunmths = (inun_yearsort['month'] >=5 )&(inun_yearsort['month']<=9)
df_inun = df_all[inunmths.reset_index(drop=True)]


#df_inun : includes only months May to September
vulner1 = []

for row in df_all['sociovulner']:
    if row <= df_inun['sociovulner'].mean()-1*df_inun['sociovulner'].std():
        vulner1.append(1)
    else:
        if row <= df_inun['sociovulner'].mean():
            vulner1.append(2)
        else:
            if row <= df_inun['sociovulner'].mean()+1*df_inun['sociovulner'].std():
                vulner1.append(3)
            else:
                if row <=df_inun['sociovulner'].mean()+2*df_inun['sociovulner'].std():
                    vulner1.append(4) 
                else:
                    vulner1.append(5)


vulner2 = []
for row in df_all['infravulner']:
    if row <= df_inun['infravulner'].mean()-1*df_inun['infravulner'].std():
        vulner2.append(5)
    else:
        if row <= df_inun['infravulner'].mean():
            vulner2.append(4)
        else:
            if row <= df_inun['infravulner'].mean()+1*df_inun['infravulner'].std():
                vulner2.append(3)
            else:
                if row <=df_inun['infravulner'].mean()+2*df_inun['infravulner'].std():
                    vulner2.append(2) 
                else:
                    vulner2.append(1)
                    
vulner3 = []
for row in df_all['phyvulner']:
    if row <= df_inun['phyvulner'].mean()-df_inun['phyvulner'].std():
        vulner3.append(5)
    else:
        if row <= df_inun['phyvulner'].mean():
            vulner3.append(4)
        else:
            if row <= df_inun['phyvulner'].mean()+1*df_inun['phyvulner'].std():
                vulner3.append(3)
            else:
                if row <=df_inun['phyvulner'].mean()+2*df_inun['phyvulner'].std():
                    vulner3.append(2) 
                else:
                    vulner3.append(1)
                    
loss1 = []
for row in df_all['prodsysloss']:
    if row <= df_inun['prodsysloss'].mean():
        loss1.append(1)
    else:
        if row <= df_inun['prodsysloss'].mean()+0.5*df_inun['prodsysloss'].std():
            loss1.append(2)
        else:
            if row <= df_inun['prodsysloss'].mean()+1*df_inun['prodsysloss'].std():
                loss1.append(3)
            else:
                if row <=df_inun['prodsysloss'].mean()+2*df_inun['prodsysloss'].std():
                    loss1.append(4) 
                else:
                    loss1.append(5)


loss2 = []
for row in df_all['infraloss']:
    if row <= df_inun['infraloss'].mean():
        loss2.append(1)
    else:
        if row <= df_inun['infraloss'].mean()+0.5*df_inun['infraloss'].std():
            loss2.append(2)
        else:
            if row <= df_inun['infraloss'].mean()+1*df_inun['infraloss'].std():
                loss2.append(3)
            else:
                if row <=df_inun['infraloss'].mean()+2*df_inun['infraloss'].std():
                    loss2.append(4) 
                else:
                    loss2.append(5)                    
                    
loss3 = []
for row in df_all['socloss']:
    if row <= df_inun['socloss'].mean():
        loss3.append(1)
    else:
        if row <= df_inun['socloss'].mean()+0.5*df_inun['socloss'].std():
            loss3.append(2)
        else:
            if row <= df_inun['socloss'].mean()+1*df_inun['socloss'].std():
                loss3.append(3)
            else:
                if row <=df_inun['socloss'].mean()+2*df_inun['socloss'].std():
                    loss3.append(4) 
                else:
                    loss3.append(5)                                        
                    
loss4 = []
for row in df_all['totalloss']:
    if row <= df_inun['totalloss'].mean():
        loss4.append(1)
    else:
        if row <= df_inun['totalloss'].mean()+0.5*df_inun['totalloss'].std():
            loss4.append(2)
        else:
            if row <= df_inun['totalloss'].mean()+1*df_inun['totalloss'].std():
                loss4.append(3)
            else:
                if row <=df_inun['totalloss'].mean()+2*df_inun['totalloss'].std():
                    loss4.append(4) 
                else:
                    loss4.append(5)     
df_all['vulner1'] = vulner1
df_all['vulner2'] = vulner2
df_all['vulner3'] = vulner3
df_all['loss1'] = loss1
df_all['loss2'] = loss2
df_all['loss3'] = loss3
df_all['loss4'] = round(df_all['loss1']+df_all['loss2']+df_all['loss3'],0)
df_all['copingdeficiency'] = round((8*df_all['vulner1']+5*df_all['vulner2']+5*df_all['vulner3'])/18,0)
df_all['damages'] = df_all['loss4']


hist_loss4 = []

# Determining max historic total loss level
rc = data['object_id'].unique()
for i in rc:
    if present_year==2021:
        k_e = 9
    elif present_year==2022:
        k_e = 21
    elif present_year==2023:
        k_e = 29
    
    for k in range(1,k_e+1):
        if k == 1:
            data_index = (data['object_id'] == i) & (data['time_stamp'] <= k)
            data_selected = df_all[data_index]
            hist_loss4.append(data_selected['loss4'].max())
        else:    
            data_index = (data['object_id'] == i) & (data['time_stamp'] < k)
            data_selected = df_all[data_index]
            hist_loss4.append(data_selected['loss4'].max())
        #print(hist_loss4)

df_all['hist_loss4'] = hist_loss4
df_all['vulnerability'] = round((0.45*df_all['copingdeficiency']+0.45*df_all['damages']+0.1*df_all['hist_loss4']),0)

inunmths = (inun_yearsort['month'] >=5 )&(inun_yearsort['month']<=9)
df_inun = df_all[inunmths]

present_data_index = (df_all['year'] == max_year_scaled) & (round(df_all['month']*11+1) == present_month)
present_data = df_all[present_data_index]
copingdeficit = list(present_data['copingdeficiency'])
damages = list(present_data['damages'])
hist_dam = list(present_data['hist_loss4'])
vulnerscore = list(present_data['vulnerability'])
socvul = list(present_data['vulner1'])
infravul = list(present_data['vulner2'])
physicalvul = list(present_data['vulner3'])
prodloss = list(present_data['loss1'])
infradam = list(present_data['loss2'])
socdam = list(present_data['loss3'])
score['socvul'] = socvul
score['infravul'] = infravul
score['physicalvul'] = physicalvul
score['copingdeficit'] = copingdeficit
score['prodloss'] = prodloss
score['infradam'] = infradam
score['socdam'] = socdam
score['damages'] = damages
score['hist_dam'] = hist_dam
score['vulnerscore'] = vulnerscore

vul_w = 2

#2D. Government Response Score
# ------------------------------

resp_prep = []
for row in df_all['cum_Preparedness']:
    if row <= df_all['cum_Preparedness'].mean():
        resp_prep.append(1)
    else:
        if row <= df_inun['cum_Preparedness'].mean()+0.5*df_inun['cum_Preparedness'].std():
            resp_prep.append(2)
        else:
            if row <= df_inun['cum_Preparedness'].mean()+1*df_inun['cum_Preparedness'].std():
                resp_prep.append(3)
            else:
                if row <=df_inun['cum_Preparedness'].mean()+2*df_inun['cum_Preparedness'].std():
                    resp_prep.append(4) 
                else:
                    resp_prep.append(5)     

resp_prep_inv = []
for row in df_all['cum_Preparedness']:
    if row <= df_all['cum_Preparedness'].mean():
        resp_prep_inv.append(5)
    else:
        if row <= df_all['cum_Preparedness'].mean()+0.5*df_all['cum_Preparedness'].std():
            resp_prep_inv.append(4)
        else:
            if row <= df_all['cum_Preparedness'].mean()+1*df_all['cum_Preparedness'].std():
                resp_prep_inv.append(3)
            else:
                if row <=df_all['cum_Preparedness'].mean()+2*df_all['cum_Preparedness'].std():
                    resp_prep_inv.append(2) 
                else:
                    resp_prep_inv.append(1)     

resp_imm = []
for row in df_all['cum_Immediate']:
    if row <= df_all['cum_Immediate'].mean():
        resp_imm.append(1)
    else:
        if row <= df_all['cum_Immediate'].mean()+0.5*df_all['cum_Immediate'].std():
            resp_imm.append(2)
        else:
            if row <= df_all['cum_Immediate'].mean()+1*df_all['cum_Immediate'].std():
                resp_imm.append(3)
            else:
                if row <=df_all['cum_Immediate'].mean()+2*df_all['cum_Immediate'].std():
                    resp_imm.append(4) 
                else:
                    resp_imm.append(5)  

resp_imm_inv = []
for row in df_all['cum_Immediate']:
    if row <= df_all['cum_Immediate'].mean():
        resp_imm_inv.append(5)
    else:
        if row <= df_all['cum_Immediate'].mean()+0.5*df_all['cum_Immediate'].std():
            resp_imm_inv.append(4)
        else:
            if row <= df_all['cum_Immediate'].mean()+1*df_all['cum_Immediate'].std():
                resp_imm_inv.append(3)
            else:
                if row <=df_all['cum_Immediate'].mean()+2*df_all['cum_Immediate'].std():
                    resp_imm_inv.append(2) 
                else:
                    resp_imm_inv.append(1)                      

resp_others = []
for row in df_all['cum_Others_tenders_awarded_value']:
    if row <= df_all['cum_Others_tenders_awarded_value'].mean():
        resp_others.append(1)
    else:
        if row <= df_all['cum_Others_tenders_awarded_value'].mean()+0.5*df_all['cum_Others_tenders_awarded_value'].std():
            resp_others.append(2)
        else:
            if row <= df_all['cum_Others_tenders_awarded_value'].mean()+1*df_all['cum_Others_tenders_awarded_value'].std():
                resp_others.append(3)
            else:
                if row <=df_all['cum_Others_tenders_awarded_value'].mean()+2*df_all['cum_Others_tenders_awarded_value'].std():
                    resp_others.append(4) 
                else:
                    resp_others.append(5)   
                    
                    

resp_others_inv = []
for row in df_all['cum_Others_tenders_awarded_value']:
    if row <= df_all['cum_Others_tenders_awarded_value'].mean():
        resp_others_inv.append(5)
    else:
        if row <= df_all['cum_Others_tenders_awarded_value'].mean()+0.5*df_all['cum_Others_tenders_awarded_value'].std():
            resp_others_inv.append(4)
        else:
            if row <= df_all['cum_Others_tenders_awarded_value'].mean()+1*df_all['cum_Others_tenders_awarded_value'].std():
                resp_others_inv.append(3)
            else:
                if row <=df_all['cum_Others_tenders_awarded_value'].mean()+2*df_all['cum_Others_tenders_awarded_value'].std():
                    resp_others_inv.append(2) 
                else:
                    resp_others_inv.append(1)   
                    
resp_total_all = []
for row in df_all['cum_total_tender_awarded_value']:
    if row <= df_all['cum_total_tender_awarded_value'].mean():
        resp_total_all.append(1)
    else:
        if row <= df_all['cum_total_tender_awarded_value'].mean()+0.5*df_all['cum_total_tender_awarded_value'].std():
            resp_total_all.append(2)
        else:
            if row <= df_all['cum_total_tender_awarded_value'].mean()+1*df_all['cum_total_tender_awarded_value'].std():
                resp_total_all.append(3)
            else:
                if row <=df_all['cum_total_tender_awarded_value'].mean()+2*df_all['cum_total_tender_awarded_value'].std():
                    resp_total_all.append(4) 
                else:
                    resp_total_all.append(5)  
                    
resp_total_all_inv = []
for row in df_all['cum_total_tender_awarded_value']:
    if row <= df_all['cum_total_tender_awarded_value'].mean():
        resp_total_all_inv.append(5)
    else:
        if row <= df_all['cum_total_tender_awarded_value'].mean()+0.5*df_all['cum_total_tender_awarded_value'].std():
            resp_total_all_inv.append(4)
        else:
            if row <= df_all['cum_total_tender_awarded_value'].mean()+1*df_all['cum_total_tender_awarded_value'].std():
                resp_total_all_inv.append(3)
            else:
                if row <=df_all['cum_total_tender_awarded_value'].mean()+2*df_all['cum_total_tender_awarded_value'].std():
                    resp_total_all_inv.append(2) 
                else:
                    resp_total_all_inv.append(1)                      

df_all['resp_prep'] = resp_prep
df_all['resp_prep_inv'] = resp_prep_inv
df_all['resp_imm'] = resp_imm
df_all['resp_imm_inv'] = resp_imm_inv
df_all['resp_others'] = resp_others
df_all['resp_others_inv'] = resp_others_inv
df_all['resp_total_all'] = resp_total_all
df_all['resp_total_all_inv'] = resp_total_all_inv

present_data_index = (df_all['year'] == max_year_scaled) & (round(df_all['month']*11+1) == present_month)
present_data = df_all[present_data_index]

resp1= list(present_data['resp_prep']) 
resp1_inv = list(present_data['resp_prep_inv'])

resp2 = list(present_data['resp_imm'])
resp2_inv = list(present_data['resp_imm_inv'])

resp3 = list(present_data['resp_others'])
resp3_inv = list(present_data['resp_others_inv'])

resp_all = list(present_data['resp_total_all'])
resp_all_inv = list(present_data['resp_total_all_inv'])

#score['resp1'] = resp1
#score['resp2'] = resp2
#score['resp3'] = resp3
#score['resp_all'] = resp_all

score['resp1_inv'] = resp1_inv
score['resp2_inv'] = resp2_inv
score['resp3_inv'] = resp3_inv
score['resp_all_inv'] = resp_all_inv

resp_w = 2
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 3: LDA
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&.
# Summative scale based model.
# --------------------------------
print('Summative scale based LDA for low elevation')

#Performing square root transformation to reduce non-normality of data.
#----------------------------------------------------------------------
df_all['totalloss_sqrt'] = np.sqrt(df_all['totalloss'])
inunmths = (inun_yearsort['month'] >=5 )&(inun_yearsort['month']<=9)
df_inun = df_all[inunmths]
# Impact levels are presently chosen as 
# Level 0: Less than or equal to mean
# Level 'n': Mean + ('n-1')*Std. Deviation < X <= Mean + ('n')*Std. Deviation
Impact_level = []
for row in df_all['totalloss_sqrt']:
    if row <= df_inun['totalloss_sqrt'].mean():
        Impact_level.append(1)
    else:
        if row <= df_inun['totalloss_sqrt'].mean()+0.5*df_inun['totalloss_sqrt'].std():
            Impact_level.append(2)
        else:
            if row <= df_inun['totalloss_sqrt'].mean()+1*df_inun['totalloss_sqrt'].std():
                Impact_level.append(3)
            else:
                if row <= df_inun['totalloss_sqrt'].mean()+2*df_inun['totalloss_sqrt'].std():
                    Impact_level.append(4) 
                else:
                    Impact_level.append(5)
df_all['Impact_level'] = Impact_level
df_inun = df_all[inunmths]

# 2A.1 LDA considering all investigative variables.
# ------------------------------------------
print("All variables")
X = df_inun[['inundation_intensity_sum','sum_population','cum_total_tender_awarded_value']]
y = df_inun['Impact_level']
model2A1 = LinearDiscriminantAnalysis(n_components = 3)
data_plot = model2A1.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5']
params2A1 = np.round(model2A1.coef_,decimals = 3)
intercept2A1 = np.round(model2A1.intercept_,decimals = 3)

print(np.round(params2A1,decimals = 1))
print(np.round(model2A1.intercept_,decimals = 3))
#creating plot to visualise how grouping is done
plt.figure()
colors = [ 'green','lime','yellow','orange','red']
lw = 2
for color, i, target_name in zip(colors, [1,2,3,4,5], target_names):
    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
                label=target_name)

#add legend to plot
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('Summative scale_Final model_low elevations')
#display LDA plot
#plt.show()

if present_year == 2021:
    pass
else:
    year_2023 = df_inun['year'] == 1
    data_2023 = df_inun[year_2023]
    head_2023 = list(df_inun.columns.values)
    data_2023 = pd.DataFrame(data = data_2023,columns = head_2023 )


    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state = 7)
    model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

    train_year = df_inun['year'] < 1
    train_data = df_inun[train_year]
    train_data = pd.DataFrame(data = train_data,columns = head_2023)

    X_train = train_data[['inundation_intensity_sum','sum_population','cum_total_tender_awarded_value']]
    X_test = data_2023[['inundation_intensity_sum','sum_population','cum_total_tender_awarded_value']]
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
df_all['totalloss_sqrt'] = np.sqrt(df_new['totalloss'])

Impact_level = []
for row in df_all['totalloss_sqrt']:
    if row <= df_new['totalloss_sqrt'].mean():
        Impact_level.append(1)
    else:
        if row <= df_new['totalloss_sqrt'].mean()+0.5*df_new['totalloss_sqrt'].std():
            Impact_level.append(2)
        else:
            if row <= df_new['totalloss_sqrt'].mean()+1*df_new['totalloss_sqrt'].std():
                Impact_level.append(3)
            else:
                if row <= df_new['totalloss_sqrt'].mean()+2*df_new['totalloss_sqrt'].std():
                    Impact_level.append(4) 
                else:
                    Impact_level.append(5)
df_all['Impact_level'] = Impact_level

# 2D.1 Including all variables of interest
# -----------------------------------------
print('All variables')
X = df_new[['sociovulner','infravulner','phyvulner','inundation_intensity_sum']]
y = df_new['Impact_level']
model2D1 = LinearDiscriminantAnalysis(n_components = 2)
data_plot = model2D1.fit(X, y).transform(X)
#print(data_plot[0:50,:])
target_names = ['1','2','3','4','5']
params2D1 = np.round(model2D1.coef_,decimals = 3)
intercept2D1 = np.round(model2D1.intercept_,decimals = 3)
print(np.round(params2D1,decimals = 1))
print(np.round(model2D1.intercept_,decimals = 3))
#creating plot to visualise how grouping is done
plt.figure()
colors = [ 'green','lime','yellow','orange','red']
lw = 2
for color, i, target_name in zip(colors, [1,2,3,4,5], target_names):
    plt.scatter(data_plot[y == i, 0], data_plot[y == i, 1], alpha=.8, color=color,
                label=target_name)

#add legend to plot
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('Summative scale_Final model_population')
#display LDA plot
#plt.show()

if present_year == 2021:
    pass
else:
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3,random_state = 7)
    model = LinearDiscriminantAnalysis(n_components = 2,solver = 'svd')

    train_year = df_new['year'] < 1
    train_data = df_new[train_year]
    train_data = pd.DataFrame(data = train_data,columns = head_2023)

    X_train = train_data[['sociovulner','infravulner','phyvulner','inundation_intensity_sum']]
    X_test = data_2023[['sociovulner','infravulner','phyvulner','inundation_intensity_sum']]
    y_train = train_data['Impact_level']
    y_test = data_2023['Impact_level']

    data_plot = model.fit(X_train, y_train).transform(X_train)
    y_pred = model.predict(X_test)
    #print(y_test)
    #print(y_pred)
    from sklearn.metrics import accuracy_score
    print(accuracy_score(y_test, y_pred))

# Modifying vulnerability score considering LDA results
# ------------------------------------------------------
sum_w = 0
for i in range(0,len(params2A1)):
    sum_w = sum_w+abs((params2A1[i][1])/params2A1[i][0])
exp1_w = sum_w/5
print(exp1_w)    

sum_w = 0
for i in range(0,len(params2A1)):
    sum_w = sum_w+abs((params2A1[i][2])/params2A1[i][0])
resp1_w = sum_w/5
print(resp1_w)    

fldhzd_w = round(0.5/(1+exp1_w+resp1_w),3)
exp_w = round(fldhzd_w*exp1_w,3)
resp_w = round(fldhzd_w*resp1_w,3)
print(fldhzd_w,exp_w,resp_w)

sum_w = 0
for i in range(0,len(params2D1)):
    sum_w = sum_w+abs((params2D1[i][0]+params2D1[i][1]+params2D1[i][2])/params2D1[i][3])
vulvar_w = sum_w/5 * fldhzd_w /.5
vul_w = 0.5
print(vulvar_w) 
 
df_all['vulnerability'] = round((vulvar_w*df_all['copingdeficiency']+(0.9-vulvar_w)*df_all['damages']+0.1*df_all['hist_loss4']),0)

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 4: TOPSIS for determining composite score
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&.

weights = [fldhzd_w,exp_w,vul_w,resp_w]

sum_weights = fldhzd_w+exp_w+vul_w+resp_w
weights = [fldhzd_w/sum_weights,exp_w/sum_weights,vul_w/sum_weights,resp_w/sum_weights]
print(weights)

scores_interest = score[["object_id","flood_hazard_score","exposurescore","vulnerscore","resp_all_inv"]]
topsis_data = scores_interest.to_numpy()
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
p_sln = np.min(topsis_data,axis = 0) #best case
n_sln = np.max(topsis_data,axis = 0) #worst case

# calculating topsis score
tscore = [] # Topsis score
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
   tscore.append(temp_p/(temp_p + temp_n))
   nn.append(temp_n)
   pp.append(temp_p)
   
data_topsis_head = ['object_id','flood_hazard_score','exposurescore','vulnerscore','resp_all_inv']
topsis_data = pd.DataFrame(data = topsis_data,columns = data_topsis_head)
topsis_data.to_csv('TOPSIS_results_mda.csv')

topsis_data['positive_dist'] = pp
topsis_data['negative_dist'] = nn
topsis_data['Topsis_Score'] = tscore


compositescorelabels = ['1','2','3','4','5']
compscore = pd.cut(topsis_data['Topsis_Score'],bins = 5,precision = 0,labels = compositescorelabels )
topsis_data['compositescore_grp'] = compscore
score['topsis_riskscore'] = compscore

# calculating the rank according to topsis score
topsis_data['Rank'] = (topsis_data['Topsis_Score'].rank(method='min', ascending=False))
topsis_data = topsis_data.astype({"Rank": int})
#additional variable included in result


topsis_data.to_csv('TOPSIS_floodproneness_jun23_mod.csv')

score['topsis_rank'] = topsis_data['Rank']

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 5: RISK FORMULA BASED SCORE
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&.
#Formula : risk score = geometric mean of (hazard^4)*(vulnerability^3)*(exposure^1)
#including government response as coping capacity in vulnerability
score['modd_vulnerscore'] = round((score['vulnerscore']+score['resp_all_inv'])/2,0)
score['formula_riskscore'] = round(((score['flood_hazard_score']**2)*(score['modd_vulnerscore']**2)*score['exposurescore'])**(1/5),0)

df_all.to_csv('df_all.csv')
score.to_csv('score.csv')
exit()

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#                               STAGE 6: DISTRICT WISE ANALYSIS
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&.

district_id = score['District'].unique()
district_pop = []
district_cumpreparedness = []
district_cumimmediate = []
district_cumtotaltenders = []

present_data_index = (df_all['year'] == max_year_scaled) & (round(df_all['month']*11+1) == present_month)
present_data = df_all[present_data_index]
district_pop = []
district_response = []

curr_dist = []
#Averaging Flood Hazard Score : Average
dist_fldhzrd = []
dist_expscore = []
dist_expscore0 = []
dist_vulnerscore = []
dist_respscore = []
dist_risk = []
score['topsis_riskscore'] = score['topsis_riskscore'].astype(int)

for j in district_id:
    curr_dist.append(j)
    district_rcscores = score[(score['District'] == j)]
    dist_fldhzrd.append(round(district_rcscores['flood_hazard_score'].mean(),0))
    dist_expscore.append(round(district_rcscores['exposurescore'].mean(),0))
    dist_vulnerscore.append(round(district_rcscores['vulnerscore'].mean(),0))
    dist_respscore.append(round(district_rcscores['resp_all_inv'].mean(),0))
    dist_risk.append(round(district_rcscores['topsis_riskscore'].mean(),0))
    
district_riskscore = pd.DataFrame(data = district_id,columns = ['District'])
district_riskscore['dist_fldhzrd'] = dist_fldhzrd
district_riskscore['dist_expscore'] = dist_expscore
district_riskscore['dist_vulnerscore'] = dist_vulnerscore
district_riskscore['dist_respscore'] = dist_respscore
district_riskscore['dist_risk'] = dist_risk

score = score.merge(district_riskscore,on = ['District'],how='left')                          

df_all.to_csv('df_all.csv')
score.to_csv('score.csv')
district_riskscore.to_csv('district_riskscore.csv')