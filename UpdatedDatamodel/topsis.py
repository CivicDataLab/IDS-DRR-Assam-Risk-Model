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

fldhzd_w = 4
exp_w = 1
vul_w = 2
resp_w = 2

weights = [fldhzd_w,exp_w,vul_w,resp_w]

sum_weights = fldhzd_w+exp_w+vul_w+resp_w
weights = [fldhzd_w/sum_weights,exp_w/sum_weights,vul_w/sum_weights,resp_w/sum_weights]
print(weights)
score = pd.read_csv('predicted_scores_2.csv')
scores_interest = score[["object_id","Hazard","Vulnerability","Exposure","Response"]]
topsis_data = (scores_interest.to_numpy()).astype(float)

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


topsis_data.to_csv('TOPSIS_jun23_new.csv')

