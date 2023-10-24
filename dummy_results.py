import pandas as pd

topsis_df = pd.read_csv('TOPSIS.csv')

date_range = pd.date_range(start="2021-05-01", end="2023-08-01", freq='MS')
# Format the date values as "YYYY_MM" strings
formatted_dates = [date.strftime('%Y_%m') for date in date_range]
# Create a Pandas DataFrame with the values
dfs = []
for year_month in formatted_dates:
    df = topsis_df.copy()
    df['timeperiod'] = year_month
    dfs.append(df)

master_df =  pd.concat(dfs).reset_index(drop = True)

master_df.to_csv('TOPSIS_dummy.csv', index = False)