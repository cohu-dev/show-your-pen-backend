import os
import json
import boto3
import uuid
import base64
from collections import deque
import io
import re
import requests
from aws_lambda_powertools import Logger
from datetime import datetime, timezone, timedelta
from PIL import Image
from PIL.Image import core as _imaging
from functions.library import utils, response, tweet

BUCKET_NAME = f"pen-bucket-dev"

s3 = boto3.resource(
    "s3",
    aws_access_key_id="S3RVER",
    aws_secret_access_key="S3RVER",
    endpoint_url="http://localhost:4569",
)
with open(os.path.join("report.json"), mode="rb") as f:
    file = f.read()
    s3.Bucket(BUCKET_NAME).put_object(Key="report.json", Body=file)
