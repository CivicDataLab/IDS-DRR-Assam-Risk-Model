from datetime import date, timedelta
import subprocess
import os

cwd = os.getcwd()
script_path = cwd+'/Sources/SENTINEL/scripts/sentinel.py'

start_date = date(2017, 4, 1)
end_date = date(2023, 9, 1)

date_list = []

while start_date <= end_date:
    date_list.append(start_date.strftime('%Y-%m-%d'))
    # Move to the first day of the next month
    if start_date.month == 12:
        start_date = start_date.replace(year=start_date.year + 1, month=1)
    else:
        start_date = start_date.replace(month=start_date.month + 1)


for idx, date_string in enumerate(date_list):
    if idx==len(date_list)-1:
         break
    else:
         date_start = date_string
         date_end = date_list[idx+1]
    
    subprocess.call(['python', script_path, date_start, date_end])

