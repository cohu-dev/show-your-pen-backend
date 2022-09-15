import json
import os
from aws_lambda_powertools import Logger
import boto3
from boto3.dynamodb.conditions import Key

STAGE = os.getenv("STAGE")
TABLE_NAME = f"pen-table-{STAGE}"


logger = Logger()


@logger.inject_lambda_context()
def handler(event, context):
    if STAGE == "dev":
        # when local
        dynamodb_resource = boto3.resource(
            "dynamodb",
            aws_access_key_id="S3RVER",
            aws_secret_access_key="S3RVER",
            endpoint_url="http://localhost:8000",
        )
    else:
        # when deploy
        dynamodb_resource = boto3.resource("dynamodb")

    table = dynamodb_resource.Table(TABLE_NAME)
    result = table.query(
        # KeyConditionExpression=Key("timestamp").gt("0"),
        # KeyConditionExpression=Key("id").gt("a") & Key("timestamp").begins_with("2021"),
        # FilterExpression=Key("id").gt("a") & Key("timestamp").begins_with("2021"),
        ScanIndexForward=True,  # True is default accend
        Limit=100,
    )
    items = result["Items"]
    logger.info(items)

    response = {
        "statusCode": 200,
        "body": json.dumps(items, default=decimal_default_proc),
    }
    return response
