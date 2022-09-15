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

LATEST_FILE = "latest.json"
MAX_LENGTH = 100
STAGE = os.getenv("STAGE")
BUCKET_NAME = f"pen-bucket-{STAGE}"
TABLE_NAME = f"pen-table-{STAGE}"
JST = timezone(timedelta(hours=+9), "JST")

logger = Logger()


@logger.inject_lambda_context()
def handler(event, context):
    body = json.loads(event["body"])
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

    image_base64_data_url = body["image"]
    __id = str(uuid.uuid4())
    filename = f"{__id}.jpg"

    # delete image type in data-url
    temp = re.sub("data:image\/.*?;base64,", "", image_base64_data_url)
    temp = temp.encode("ascii")
    byte = base64.b64decode(temp)

    # rekognition
    rekognition_client = boto3.client("rekognition")
    res = rekognition_client.detect_labels(
        Image={"Bytes": byte},
        MaxLabels=10,
        MinConfidence=70,
    )
    if not utils.get_is_pen(res):
        logger.info("this is not a pen")
        return response._400({"message": "この写真からペンは検出されませんでした。もう少しペンを大きく写してください。"})

    # put file & get width, height
    temp_path = utils.get_temp_path(STAGE, filename)
    image = Image.open(io.BytesIO(byte)).convert("RGB")
    image = utils.scale_to_width(image, 500)
    image.save(temp_path, format="jpeg")
    width, height = image.size

    # file save to S3
    with open(temp_path, mode="rb") as f:
        file = f.read()
        s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=file)

    item = {
        "id": __id,
        "timestamp": datetime.now(JST).isoformat(),
        "filename": f"{__id}.jpg",
        "width": width,
        "height": height,
    }
    table = dynamodb_resource.Table(TABLE_NAME)
    table.put_item(Item=item)

    latest_obj = s3.Object(BUCKET_NAME, LATEST_FILE)
    latest_con = latest_obj.get()["Body"].read().decode("utf-8")
    latest_json = json.loads(latest_con)
    latest_json = deque(latest_json, MAX_LENGTH)
    latest_json.appendleft(item)
    latest_obj.put(
        Body=json.dumps(list(latest_json), default=utils.decimal_default_proc),
        ContentType="application/json",
    )

    # tweet
    try:
        twi = tweet.TwitterAPI()
        twi.upload_realtime(temp_path)
        logger.info(f"tweet image {filename}")
    except:
        logger.info(f"twitter api fail")
    # for number of times uploading
    os.remove(temp_path)

    return response._200(
        {
            "message": "投稿に成功しました",
        }
    )
