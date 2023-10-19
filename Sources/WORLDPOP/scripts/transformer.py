import pandas as pd
import glob
import os
data_path = os.getcwd()+'/Sources/WORLDPOP/data/'


files = glob.glob(data_path+'worldpopstats_*.csv')
dfs = []
for file in files:
    df = pd.read_csv(file)
    df['year'] = int(file.split('_')[-1][:-4])
    dfs.append(df)

master_df = pd.concat(dfs)
master_df = master_df.sort_values(by='year').reset_index(drop=True)

projection_files = glob.glob(data_path+'*_projections.csv')
dfs = [pd.read_csv(projection_files[0])]
for file in projection_files[1:]:
    df = pd.read_csv(file)
    dfs.append(df.drop(['year','object_id'], axis=1))


projection_df = pd.concat(dfs, axis=1)

result = pd.concat([master_df[projection_df.columns], projection_df])

variables = result.drop(['object_id', 'year'], axis=1).columns
for variable in variables:
    variable_df = result[['object_id', 'year', variable]]

    for year in result.year.unique():
        variable_df_yearly = variable_df[variable_df['year'] == year]
        variable_df_yearly = variable_df_yearly.drop(['year'], axis=1)

        if os.path.exists(data_path+'variables/'+variable):
            variable_df_yearly.to_csv(data_path + 'variables/' + variable+'/{}_{}.csv'.format(variable, year), index=False)
        else:
            os.mkdir(data_path+'variables/'+variable)
            variable_df_yearly.to_csv(data_path + 'variables/' + variable+'/{}_{}.csv'.format(variable, year), index=False)
