import io
import json
import os
from aws_lambda_powertools import Logger
import boto3
from functions.library import utils, response

LATEST_FILE = "latest.json"
MAX_LENGTH = 100
STAGE = os.getenv("STAGE")
BUCKET_NAME = f"pen-bucket-{STAGE}"
TABLE_NAME = f"pen-table-{STAGE}"


logger = Logger()


@logger.inject_lambda_context()
def handler(event, context):
    if STAGE == "dev":
        # when local
        s3 = boto3.resource(
            "s3",
            aws_access_key_id="S3RVER",
            aws_secret_access_key="S3RVER",
            endpoint_url="http://localhost:4569",
        )
    else:
        # when deploy
        s3 = boto3.resource("s3")
    latest_obj = s3.Object(BUCKET_NAME, LATEST_FILE)
    latest_con = latest_obj.get()["Body"].read().decode("utf-8")
    latest_json = json.loads(latest_con)
    return response._200(list(latest_json))
