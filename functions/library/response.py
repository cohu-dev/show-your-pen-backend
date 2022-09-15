import os
import json
from decimal import Decimal
from functions.library import utils

API_ALLOW_ORIGIN = "https://pen.cohu.dev"


def _200(val=None):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": API_ALLOW_ORIGIN,
            "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(
            val if val is not None else "no response data",
            default=utils.decimal_default_proc,
        ),
    }


def _400(val=None):
    return {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": API_ALLOW_ORIGIN,
            "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(
            val if val is not None else "no response data",
            default=utils.decimal_default_proc,
        ),
    }


def _500(val=None):
    return {
        "statusCode": 500,
        "headers": {
            "Access-Control-Allow-Origin": API_ALLOW_ORIGIN,
            "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(
            val if val is not None else "no response data",
            default=utils.decimal_default_proc,
        ),
    }
