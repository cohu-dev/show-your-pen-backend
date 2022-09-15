import os
import json
import boto3
import uuid
import base64
import io
import re
import glob
from aws_lambda_powertools import Logger
BUCKET_NAME = f"pen-bucket-dev"
with open("data/latest.json","rb") as f:
    file = f.read()
    s3 = boto3.resource(
        "s3",
        aws_access_key_id="S3RVER",
        aws_secret_access_key="S3RVER",
        endpoint_url="http://localhost:4569",
    )
    s3.Bucket(BUCKET_NAME).put_object(Key="latest.json", Body=file)

