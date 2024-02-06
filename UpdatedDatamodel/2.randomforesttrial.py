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
from sklearn.ensemble import RandomForestClassifier
from random import randint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from imblearn.over_sampling import RandomOverSampler # For oversampling and undersampling
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_validate
#Visualizing tree
from sklearn.tree import export_graphviz
import pydot
from sklearn.metrics import precision_recall_fscore_support as score

#defining oversampling strategy
# ------------------------------
oversampler = RandomOverSampler(random_state = 0)

features = pd.read_csv('floodhazard.csv')
#features[['Jan','Feb','March','Apr','May','June','July','Aug','Sep','Oct','Nov','Dec']] = pd.get_dummies(features['month'],dtype = int)
features[['2021','2022','2023']] = pd.get_dummies(features['year'],dtype = int)

rc = features['object_id'].unique()

#Computing historic averages for baseline 
#0.1 Creating timeline id
# ------------------------

p = 0

conditions = [(features['year'] == 2021)&(features['month'] == 4),
(features['year'] == 2021)&(features['month'] == 5),(features['year'] == 2021)&(features['month'] == 6),
(features['year'] == 2021)&(features['month'] == 7),(features['year'] == 2021)&(features['month'] == 8),
(features['year'] == 2021)&(features['month'] == 9),(features['year'] == 2021)&(features['month'] == 10),
(features['year'] == 2021)&(features['month'] == 11),(features['year'] == 2021)&(features['month'] == 12),
(features['year'] == 2022)&(features['month'] == 1),(features['year'] == 2022)&(features['month'] == 2),
(features['year'] == 2022)&(features['month'] == 3),(features['year'] == 2022)&(features['month'] == 4),
(features['year'] == 2022)&(features['month'] == 5),(features['year'] == 2022)&(features['month'] == 6),
(features['year'] == 2022)&(features['month'] == 7),(features['year'] == 2022)&(features['month'] == 8),
(features['year'] == 2022)&(features['month'] == 9),(features['year'] == 2022)&(features['month'] == 10),
(features['year'] == 2022)&(features['month'] == 11),(features['year'] == 2022)&(features['month'] == 12),
(features['year'] == 2023)&(features['month'] == 1),(features['year'] == 2023)&(features['month'] == 2),
(features['year'] == 2023)&(features['month'] == 3),(features['year'] == 2023)&(features['month'] == 4),
(features['year'] == 2023)&(features['month'] == 5),(features['year'] == 2023)&(features['month'] == 6),
(features['year'] == 2023)&(features['month'] == 7),(features['year'] == 2023)&(features['month'] == 8)
]

values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
features['time_stamp'] = np.select(conditions,values)

hist_hazardclass = []
month = []
year = []
RC = []

present_year = 2023

#1.1 Computing Historic Averages for Losses and Damages
#----------------------------------------------------
for i in rc:
    for j in range(2021,present_year + 1):
            if j == 2021:
                for k in range(1,13):
                    month.append(k)
                    year.append(j)
                    RC.append(i)
                    data_index = (features['object_id'] == i) & (features['year'] == j) & (features['month'] == k)
                    data_selected = features[data_index]
                    hist_hazardclass.append(round(data_selected['Hazard class'].mean(),0))
            else:
                if j == 2022:
                    for k in range(1,5):
                        month.append(k)
                        year.append(j)
                        RC.append(i)
                        data_index = (features['object_id'] == i) & (features['year'] == j) & (features['month'] == k)
                        data_selected = features[data_index]
                        hist_hazardclass.append(round(data_selected['Hazard class'].mean(),0))
                    for k in range(5,13):
                        month.append(k)
                        year.append(j)
                        RC.append(i)
                        data_index = (features['object_id'] == i) & (features['year'] < j) & (features['month'] == k)
                        data_selected = features[data_index]
                        hist_hazardclass.append(round(data_selected['Hazard class'].mean(),0))
                else:
                    for k in range(1,13):
                        month.append(k)
                        year.append(j)
                        RC.append(i)
                        data_index = (features['object_id'] == i) & (features['year'] < j) & (features['month'] == k)
                        data_selected = features[data_index]
                        hist_hazardclass.append(round(data_selected['Hazard class'].mean(),0))
        
                                              
historic_data = pd.DataFrame(data = RC,columns = ['object_id'])
historic_data['year'] = year
historic_data['month'] = month
historic_data['hist_hazardclass'] = hist_hazardclass


#1.a Merging data with master file
#----------------------------------
features = features.merge(historic_data,on = ['object_id','year','month'],how = 'left')
features.to_csv('features.csv')

labels = np.array(features['Hazard class'])

features = features.drop('Hazard class',axis = 1)
features = features.drop(['object_id','month','year','inundation_pct','inundation_intensity_mean','inundation_intensity_mean_nonzero','inundation_intensity_sum','time_stamp'],axis = 1)
features = features.drop(['max_rain','mean_rain','sum_rain','mean_ndvi','ndbi_mean','hist_hazardclass'],axis = 1)
#features = features.drop(['prev1_maxrain','prev1_meanrain','prev1_sumrain','prev2_maxrain','prev2_meanrain','prev2_sumrain','prev1_inunpct','prev1_inunmeannonzero','prev1_inunsum'],axis = 1)
features = features.drop(['2021','2022','2023'],axis = 1)
feature_list = list(features.columns)

features = np.array(features)

over_features,over_labels = oversampler.fit_resample(features,labels)

over_train_features, over_test_features, over_train_lables, over_test_labels = train_test_split(over_features, over_labels, test_size = 0.25)

print('Training features shape: ',over_train_features.shape)
print('Training labels shape: ', over_train_lables.shape)
print('Test features shape: ',over_test_features.shape)
print('Test labels shape:', over_test_labels.shape)

# Baseline prediction : Historical averages
#baseline_preds = over_test_features[:,feature_list.index('hist_hazardclass')]

#Baseline error 
#baseline_errors = abs(baseline_preds - over_test_labels)

#print('Average baseline error: ',round(np.mean(baseline_errors),2))
#############################################################################################################
# Random Forest Classifier


rf = RandomForestClassifier(n_estimators = 175,max_depth = 17,random_state = 42)
#rf.fit(train_features,train_lables);

#cv = RepeatedStratifiedKFold(n_splits = 10, n_repeats = 3, random_state = 1)
#scoring = ('f1','recall','precision')

#scores = cross_validate(rf,over_features,over_labels,scoring = scoring,cv=cv)
#print('Mean f1: %.3f' % mean(scores['test_f1']))
#print('Mean recall: %.3f' % mean(scores['test_recall']))
#print('Mean precision: %.3f' % mean(scores['test_precision']))

train_features, test_features, train_lables, test_labels = train_test_split(features, labels, test_size = 0.25,random_state = 42)
rf.fit(over_train_features,over_train_lables)

print('Test features shape: ',test_features.shape)
print('Test labels shape:', test_labels.shape)

predictions = rf.predict(test_features)
errors = abs(predictions - test_labels)
print('mean absolute error: ',round(np.mean(errors),2))

mape = 100*(errors/test_labels)

accuracy = 100 - np.mean(mape)
print('Accuracy: ',round(accuracy,2),'%')

tree = rf.estimators_[5]
export_graphviz(tree,out_file = 'tree.dot',feature_names = feature_list,rounded = True, precision = 1)
(graph, ) = pydot.graph_from_dot_file('tree.dot')

graph.write_png('tree.png')

rf_small = RandomForestClassifier(n_estimators = 10,max_depth = 3)
rf_small.fit(over_train_features,over_train_lables)

tree_small = rf_small.estimators_[5]

export_graphviz(tree_small,out_file = 'small_tree.dot',feature_names = feature_list, rounded = True, precision = 1)
(graph, ) = pydot.graph_from_dot_file('small_tree.dot')
graph.write_png('small_tree.png')

precision, recall, fscore, support = score(test_labels, predictions)

print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))

cm = confusion_matrix(test_labels,predictions)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.show()
plt.close()

#accuracy = accuracy_score(test_labels,predictions)
#precision = precision_score(test_labels,predictions)
#recall == recall_score(test_labels,predictions)

#print("Accuracy: ",accuracy)
#print("Precision: ",precision)
#print("Recall: ",recall)

feature_importances = pd.Series(rf.feature_importances_,index = feature_list).sort_values(ascending = False)
feature_importances.plot.bar()
plt.show()
plt.close()

# predicting for june 23

indes = pd.read_csv('june23interest.csv')

conditions = [(indes['year'] == 2021)&(indes['month'] == 4),
(indes['year'] == 2021)&(indes['month'] == 5),(indes['year'] == 2021)&(indes['month'] == 6),
(indes['year'] == 2021)&(indes['month'] == 7),(indes['year'] == 2021)&(indes['month'] == 8),
(indes['year'] == 2021)&(indes['month'] == 9),(indes['year'] == 2021)&(indes['month'] == 10),
(indes['year'] == 2021)&(indes['month'] == 11),(indes['year'] == 2021)&(indes['month'] == 12),
(indes['year'] == 2022)&(indes['month'] == 1),(indes['year'] == 2022)&(indes['month'] == 2),
(indes['year'] == 2022)&(indes['month'] == 3),(indes['year'] == 2022)&(indes['month'] == 4),
(indes['year'] == 2022)&(indes['month'] == 5),(indes['year'] == 2022)&(indes['month'] == 6),
(indes['year'] == 2022)&(indes['month'] == 7),(indes['year'] == 2022)&(indes['month'] == 8),
(indes['year'] == 2022)&(indes['month'] == 9),(indes['year'] == 2022)&(indes['month'] == 10),
(indes['year'] == 2022)&(indes['month'] == 11),(indes['year'] == 2022)&(indes['month'] == 12),
(indes['year'] == 2023)&(indes['month'] == 1),(indes['year'] == 2023)&(indes['month'] == 2),
(indes['year'] == 2023)&(indes['month'] == 3),(indes['year'] == 2023)&(indes['month'] == 4),
(indes['year'] == 2023)&(indes['month'] == 5),(indes['year'] == 2023)&(indes['month'] == 6),
(indes['year'] == 2023)&(indes['month'] == 7),(indes['year'] == 2023)&(indes['month'] == 8)
]

values = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
indes['time_stamp'] = np.select(conditions,values)
#indes[['Jan','Feb','March','Apr','May','June','July','Aug','Sep','Oct','Nov','Dec']] = 0
#indes[['June']] = 1

indes = indes.drop('Hazard class',axis = 1)
indes = indes.drop(['object_id','month','year','inundation_pct','inundation_intensity_mean','inundation_intensity_mean_nonzero','inundation_intensity_sum','time_stamp'],axis = 1)
indes = indes.drop(['max_rain','mean_rain','sum_rain','mean_ndvi','ndbi_mean'],axis = 1)
#indes = indes.drop(['prev1_maxrain','prev1_meanrain','prev1_sumrain','prev2_maxrain','prev2_meanrain','prev2_sumrain','prev1_inunpct','prev1_inunmeannonzero','prev1_inunsum'],axis = 1)


indes_predict = rf.predict(indes)
indes_predict= pd.DataFrame(indes_predict)
indes_predict.to_csv('predicted_scores.csv')
