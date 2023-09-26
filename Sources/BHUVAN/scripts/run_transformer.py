from datetime import date, timedelta
import subprocess
import os
import glob

cwd = os.getcwd()
path = os.getcwd()+'/Sources/BHUVAN/'
script_path = cwd+'/Sources/BHUVAN/scripts/transformer.py'

for year in range(2015,2024):
    print(year)
    year = str(year)
    for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        files1 = glob.glob(path+"data/tiffs/removed_watermarks/"+year+"_??_"+month+"*.tif")
        files2 = glob.glob(path+"data/tiffs/removed_watermarks/"+year+"_??-??_"+month+"*.tif")
        files = files1+files2
        if len(files)==0:
            print('No files for the month')
            continue
        else:
            print('Number of images:', len(files))
            subprocess.call(['python3', script_path, year, month])
