import pandas as pd
import os

path = os.getcwd()

#df = pd.read_excel(path+'/Sources/ANTYODAYA/output/antyodaya_village_dataset_with_revenue_circle.xlsx')
df = pd.read_excel(path+'/Sources/ANTYODAYA/input/MissionAntyodaya2020_Assam.xlsx')
print(df.shape)