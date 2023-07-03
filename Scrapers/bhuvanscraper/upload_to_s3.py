import glob
import boto3
from decouple import config
import time
from multiprocessing.pool import ThreadPool

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
    s3.Bucket('bhuvanscraper').upload_file(Filename=file_path, Key="2016/"+str(image_name))
    return None

tic = time.perf_counter()
pool = ThreadPool(processes=4)
pool.map(upload_tif, result)
toc = time.perf_counter()
print("Time Taken: {} seconds".format(toc-tic))

