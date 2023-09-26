import os
import glob
import pandas as pd
import re

#BHUVAN
path = os.getcwd()+'/Sources/BHUVAN/data/inundation_pct/'
csvs = glob.glob(path+'*.csv')
dfs= []
for csv in csvs:
    month = re.findall(r'\d{4}_\d{2}', csv)[0]
    df = pd.read_csv(csv)
    df['month'] = month
    dfs.append(df)

master_df = pd.concat(dfs)

master_df.to_csv(os.getcwd()+'/Sources/archive/inundation.csv', index=False)