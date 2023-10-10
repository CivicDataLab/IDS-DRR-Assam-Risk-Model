import pandas as pd
import glob
import os
path = os.getcwd()+'/Sources/WORLDPOP/'


files = glob.glob(path+'data/worldpopstats_*.csv')
dfs = []
for file in files:
    df = pd.read_csv(file)
    df['year'] = int(file.split('_')[-1][:-4])
    dfs.append(df)

master_df = pd.concat(dfs)
master_df = master_df.sort_values(by='year').reset_index(drop=True)

projection_files = glob.glob(path+'data/*_projections.csv')
dfs = [pd.read_csv(projection_files[0])]
for file in projection_files[1:]:
    df = pd.read_csv(file)
    dfs.append(df.drop(['year','object_id'], axis=1))


projection_df = pd.concat(dfs, axis=1)

result = pd.concat([master_df[projection_df.columns], projection_df])
result.to_csv(path+'data/worldpopstats_archive.csv', index=False)