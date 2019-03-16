# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/16
import requests
import json
from tools import timestamp_to_time


def do_get(lat, lon):
    """ 请求
    :param lat: 纬度
    :param lon: 经度
    :return: 本次请求的images
    """
    home = "https://api.caiyunapp.com/v1/radar/images"
    params = {
        "lon" : lon, # 118.081
        "lat" : lat, # 24.48176
        "token" : "Y2FpeXVuIGFuZHJpb2QgYXBp",
        "level" : 1,
        "device_id" : "99001113012363"
    }
    r = requests.get(home, params=params)
    json_str = r.text
    ret = json.loads(json_str)
    if "images" not in ret:
        return None
    imgs = ret["images"]
    for image in imgs:
        image[1] = timestamp_to_time(image[1]) # 转换时间
    return imgs