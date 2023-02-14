import boto3
import os
from main import *
import json

# Authenticate to AWS in - file
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "~/qtrobot/.aws_credentials/credentials.json"

# Open the credentials json file
with open(os.environ['AWS_SHARED_CREDENTIALS_FILE']) as f:
    data = json.load(f)

accesskey = data['AWS']['aws_access_key_id']
secretkey = data['AWS']['aws_secret_access_key']

s3_client = boto3.client('s3', region_name='eu-west-2',
                         aws_access_key_id=accesskey, aws_secret_access_key=secretkey)

# Defining the upload service


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client.upload_file(file_name, bucket, object_name)
