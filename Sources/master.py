import os
import glob
import pandas as pd
import re
main_directory = os.getcwd()+'/Sources/'

# Iterate through all folders and sub-folders
for root, dirs, files in os.walk(main_directory):
    if 'variables/' in root:
        #print(root)
        csv_files = glob.glob(root+'/*.csv')
        dfs= []
        for csv in csv_files:
            if any([x in csv for x in ['BHARATMAPS', 'GCN250', 'NASADEM', 'NERDRR', 'ANTYODAYA']]): # snapshot sources
                timeperiod = ''
                file_name = csv_files[0].split('/')[-1][:-4]
            elif any([x in csv for x in ['WORLDPOP', 'WRIS']]):
                timeperiod = re.findall(r'\d{4}', csv)[0] #year
                file_name = csv_files[0].split('/')[-1][:-9]
            elif 'SENTINEL' in csv:
                timeperiod = re.findall(r'\d{4}-\d{2}-\d{2}', csv)[0]
                timeperiod = timeperiod[:-3]
                timeperiod = timeperiod.replace('-', '_')
                file_name = csv_files[0].split('/')[-1][:-15]
            else:
                timeperiod = re.findall(r'\d{4}_\d{2}', csv)[0]
                file_name = csv_files[0].split('/')[-1][:-12]
            df = pd.read_csv(csv)
            df['timeperiod'] = timeperiod
            dfs.append(df)

        master_df = pd.concat(dfs)
        master_df.to_csv(main_directory+'master/{}.csv'.format(file_name),
                         index=False)

    else:
        pass
    
#IMD
path = os.getcwd()+'/Sources/IMD/data/rain/csv/'
csvs = glob.glob(path+'*.csv')
dfs= []
for csv in csvs:
    month = re.findall(r'\d{4}_\d{2}', csv)[0]
    df = pd.read_csv(csv)
    df['timeperiod'] = month
    dfs.append(df)


master_df = pd.concat(dfs)
master_df = master_df.rename(columns={'max': 'max_rain', 'mean':'mean_rain', 'sum':'sum_rain'})
master_df.to_csv(os.getcwd()+'/Sources/master/rainfall.csv', index=False)

#BHUVAN
path = os.getcwd()+'/Sources/BHUVAN/data/variables/inundation_pct/'
csvs = glob.glob(path+'*.csv')
dfs= []
for csv in csvs:
    month = re.findall(r'\d{4}_\d{2}', csv)[0]
    df = pd.read_csv(csv)
    df['timeperiod'] = month
    dfs.append(df)

master_df = pd.concat(dfs)
master_df.to_csv(os.getcwd()+'/Sources/master/inundation.csv', index=False)