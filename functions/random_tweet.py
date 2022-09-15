import io
import json
import os
import re
import uuid
from aws_lambda_powertools import Logger
import boto3
from boto3.dynamodb.conditions import Key
from .utils import *
import requests
from aws_lambda_powertools import Logger
from datetime import datetime, timezone, timedelta
from PIL import Image
from PIL.Image import core as _imaging
from functions.library import utils, response, tweet

STAGE = os.getenv("STAGE")
TABLE_NAME = f"pen-table-{STAGE}"


logger = Logger()
from decimal import Decimal


@logger.inject_lambda_context()
def handler(event, context):
    return response._200()
