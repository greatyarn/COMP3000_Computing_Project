import boto3
from main import *

s3_client = boto3.client('s3', region_name=eu-west-2, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client.upload_file(file_name, bucket, object_name)
