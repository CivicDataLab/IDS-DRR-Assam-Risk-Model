import glob
import boto3
from decouple import config
import time
from multiprocessing.pool import ThreadPool

import os
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

cwd = os.getcwd()
result = glob.glob(cwd+'Sources/BHUVAN/data/tiffs/*.{}'.format('tif'))

bucket_name = 'ids-drr'
s3 = boto3.client(service_name='s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name='ap-south-1')

for root, dirs, files in os.walk(cwd+'/Sources/BHUVAN/data/'):
    if '.ipynb_checkpoints' in root:
        continue
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, cwd+'/Sources/BHUVAN/data/')
        print(relative_path)

        s3_path = os.path.join('bhuvan', relative_path)
        try:
            s3.upload_file(local_path, bucket_name, s3_path)
            print(f'Successfully uploaded {local_path} to {bucket_name}/{s3_path}')
        except Exception as e:
            print(f'Error uploading {local_path} to {bucket_name}/{s3_path}: {e}')

exit()

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

result = glob.glob('tiffs/*.{}'.format('tif'))
print(len(result))
s3 = boto3.resource(
        service_name='s3',
        region_name='ap-south-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_tif(file_path):
    image_name = file_path.split("/")[1]
    print(image_name)
    s3.Bucket('ids-drr').upload_file(Filename=file_path, Key="2016/"+str(image_name))
    return None

tic = time.perf_counter()
pool = ThreadPool(processes=4)
pool.map(upload_tif, result)
toc = time.perf_counter()
print("Time Taken: {} seconds".format(toc-tic))

