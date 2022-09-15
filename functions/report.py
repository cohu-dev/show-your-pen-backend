import json
import os
import boto3
from aws_lambda_powertools import Logger
import requests
from functions.library import response, utils


logger = Logger()
X_API_KEY = os.getenv("X_API_KEY")
STAGE = os.getenv("STAGE")
DELETE_URL = os.getenv("DELETE_URL")
S3_PRD_URL = os.getenv("S3_PRD_URL")
WEBHOOK_REPORT_URL = os.getenv("WEBHOOK_REPORT_URL")
REPORT_FILE = "report.json"
BUCKET_NAME = f"pen-bucket-{STAGE}"


@logger.inject_lambda_context()
def handler(event, context):
    path_params = event.get("pathParameters")
    pen_id = path_params.get("id")

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

    report_obj = s3.Object(BUCKET_NAME, REPORT_FILE)
    report_con = report_obj.get()["Body"].read().decode("utf-8")
    report_json = json.loads(report_con)
    if pen_id in report_json:
        logger.info("already reported")
        return response._200()
    else:
        report_json.append(pen_id)
    report_obj.put(
        Body=json.dumps(report_json, default=utils.decimal_default_proc),
        ContentType="application/json",
    )
    delete_url = (
        f"{DELETE_URL}/{pen_id}"
        if STAGE == "prd"
        else f"http://localhost:3000/dev/pen/{pen_id}"
    )
    s3_image_url = (
        f"{S3_PRD_URL}/{pen_id}.jpg"
        if STAGE == "prd"
        else f"https://localhost:4569/pen-bucket-dev/{pen_id}.jpg"
    )
    requests.post(
        data=json.dumps(
            {
                "text": f"{pen_id}：の画像が報告を受けました。\n\n<https://pen.cohu.dev|ページリンク>\n\n削除したい場合はcurlしてください。\n\n```curl --location --request DELETE {delete_url} --header 'X-Api-Key:{X_API_KEY}'```",
                "attachments": [
                    {
                        "image_url": s3_image_url,
                    }
                ],
            }
        ),
        url=WEBHOOK_REPORT_URL,
    )
    return response._200()
