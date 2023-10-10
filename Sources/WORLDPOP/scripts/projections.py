import pandas as pd
import glob
import os
path = os.getcwd()+'/Sources/WORLDPOP/'
import sys
global projected_variable
projected_variable = sys.argv[1]

files = glob.glob(path+'data/worldpopstats_*.csv')
dfs = []
for file in files:
    df = pd.read_csv(file)
    df['year'] = int(file.split('_')[-1][:-4])
    dfs.append(df)

master_df = pd.concat(dfs)
master_df = master_df.sort_values(by='year').reset_index(drop=True)

# Define a function to extrapolate population for a given state
def extrapolate_variable(rc_data):
    years = rc_data['year'].tolist()
    sum_population_values = rc_data[projected_variable].tolist()

    # Calculate the average annual growth rate
    average_growth_rate = (sum_population_values[-1] - sum_population_values[0]) / (len(years) - 1)

    # Extrapolate population for the next 3 years (2021, 2022, and 2023)
    extrapolated_values = []
    for year in range(2021, 2024):
        estimated_value = sum_population_values[-1] + (average_growth_rate * (year - years[-1]))
        extrapolated_values.append(estimated_value)

    return extrapolated_values

# Group the data by state and apply the extrapolation function to each group
extrapolated_data = master_df.groupby('object_id').apply(extrapolate_variable)

# Create a new DataFrame from the extrapolated data
extrapolated_df = pd.DataFrame(extrapolated_data.tolist(), columns=['2021', '2022', '2023'])
extrapolated_df.index = extrapolated_data.index
extrapolated_df = extrapolated_df.reset_index()

extrapolated_df = pd.melt(extrapolated_df, id_vars=['object_id'], var_name='year', value_name=projected_variable)
# Add state and years columns to the extrapolated DataFrame
#extrapolated_df['object_id'] = df['object_id'].unique()
#extrapolated_df['year'] = [2021, 2022, 2023]

# Reorder the columns
#extrapolated_df = extrapolated_df[['year', 'object_id', 2021, 2022, 2023]]

extrapolated_df.to_csv(path+'data/'+projected_variable+'_projections.csv', index=False)