import boto3
from main import *

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client.upload_file(file_name, bucket, object_name)
