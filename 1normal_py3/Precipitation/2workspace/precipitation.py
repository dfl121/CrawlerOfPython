# coding : utf8
# @Author : PasserQi
# @Version : v1.0 2019/3/9
import requests
import json
import time

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

def check_extent(img):
    extent = img[2]
    pass

def time_to_timestamp(t):
    return time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))

def timestamp_to_time(c):
    return time.strftime("%Y/%m/%d %H:%M", time.localtime(c) )

images = []
if __name__ == '__main__':
    do_get(24.48176, 118.081)

    print "1"

