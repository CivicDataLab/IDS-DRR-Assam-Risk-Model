import os
import glob
from decouple import config
import boto3

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

cwd = os.getcwd()

sources = ['FRIMS', 'TENDERS', 'FFS', 'ANTYODAYA', 'SENTINEL', 'GCN250', 'WRIS',
           'NERDRR', 'IMD', 'WORLDPOP', 'NASADEM', 'BHUVAN', 'BHARATMAPS']
bucket_name = 'ids-drr'
s3 = boto3.client(service_name='s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name='ap-south-1')


for source in sources:
    print(source)
    try:
        files_in_s3 = []
        for key in s3.list_objects_v2(Bucket=bucket_name, Prefix=source)['Contents']:
            files_in_s3.append(key['Key'].split('data')[1])
    except:
        pass
    
    # Uploading variables only
    for root, dirs, files in os.walk(cwd+'/Sources/{}/data/variables/'.format(source)):
        if '.ipynb_checkpoints' in root:
            continue
        for file in files:
            local_path = os.path.join(root, file)

            #Use this code to skip uploading if the file is already in s3 bucket. Overwrites otherwise
            if local_path.split('data')[1] in files_in_s3:
                continue

            #relative path will decide the folder structure inside S3 bucket
            relative_path = os.path.relpath(local_path, cwd+'/Sources/{}/'.format(source))
            print('\n')
            print(relative_path)


            s3_path = os.path.join(source, relative_path)
            try:
                s3.upload_file(local_path, bucket_name, s3_path)
                print(f'Successfully uploaded {local_path} to {bucket_name}/{s3_path}')
            except Exception as e:
                print(f'Error uploading {local_path} to {bucket_name}/{s3_path}: {e}')