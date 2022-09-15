import os
from decimal import Decimal


def get_is_pen(res: dict) -> bool:
    flag = False
    for label in res["Labels"]:
        if label["Name"] in ("Pen", "Pencil", "Fountain Pen"):
            flag = True
            break
    return flag


def get_temp_path(stage, filename):
    if stage == "dev":
        return os.path.join("tmp", filename)
    else:
        return f"/tmp/{filename}"


def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def scale_to_width(img, width):
    height = round(img.height * width / img.width)
    return img.resize((width, height))
