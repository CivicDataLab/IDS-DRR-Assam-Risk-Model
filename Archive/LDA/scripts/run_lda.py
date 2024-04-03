from datetime import date, timedelta
import subprocess
import os

cwd = os.getcwd()
path = os.getcwd()+'/Sources/BHUVAN/'
script_path = cwd+'/LDA/scripts/master_datacode_mda.py'

for year in range(2022,2024):
    print(year)
    year = str(year)
    for month in range(1,13):
        subprocess.call(['python3', script_path, str(year), str(month)])
