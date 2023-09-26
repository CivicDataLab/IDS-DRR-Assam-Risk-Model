import os
import glob

import boto3

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

cwd = os.getcwd()
result = glob.glob('tiffs/*.{}'.format('tif'))

bucket_name = 'ids-drr'
s3 = boto3.client(service_name='s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name='ap-south-1')

for root, dirs, files in os.walk(cwd+'/Sources/SENTINEL/data/'):
    if '.ipynb_checkpoints' in root:
        continue
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, cwd+'/Sources/SENTINEL/data/')
        print(relative_path)

        s3_path = os.path.join('sentinel', relative_path)
        try:
            s3.upload_file(local_path, bucket_name, s3_path)
            print(f'Successfully uploaded {local_path} to {bucket_name}/{s3_path}')
        except Exception as e:
            print(f'Error uploading {local_path} to {bucket_name}/{s3_path}: {e}')

