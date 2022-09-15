import json
import os
from aws_lambda_powertools import Logger
import boto3
from aws_lambda_powertools import Logger
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
        dynamodb_resource = boto3.resource(
            "dynamodb",
            aws_access_key_id="S3RVER",
            aws_secret_access_key="S3RVER",
            endpoint_url="http://localhost:8000",
        )
    else:
        # when deploy
        s3 = boto3.resource("s3")
        dynamodb_resource = boto3.resource("dynamodb")

    # get id
    path_params = event.get("pathParameters")
    pen_id = path_params.get("id")

    # delete_item
    table = dynamodb_resource.Table(TABLE_NAME)
    table.delete_item(Key={"id": pen_id})

    # get latest.json
    latest_obj = s3.Object(BUCKET_NAME, LATEST_FILE)
    latest_con = latest_obj.get()["Body"].read().decode("utf-8")
    latest_dict = json.loads(latest_con)

    # delete key-value
    for i in range(len(latest_dict)):
        if latest_dict[i].get("id") == pen_id:
            del latest_dict[i]
            break

    # put latest.json
    latest_obj.put(
        Body=json.dumps(list(latest_dict), default=utils.decimal_default_proc),
        ContentType="application/json",
    )

    return response._200()
