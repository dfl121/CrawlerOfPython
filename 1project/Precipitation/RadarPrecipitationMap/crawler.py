# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/16
import requests
import json
from tools import timestamp_to_time
from collections import OrderedDict

# debug
from tools import save_json

# 图幅的中心点
global request_points
request_points = OrderedDict()

def do_get(lat, lon):
    """ 请求
    :param lat: 纬度
    :param lon: 经度
    :return:
        本次请求的images
            [0]: 图片url
            [1]：时间
            [2]：extent
        返回失败None
    """
    home = "https://api.caiyunapp.com/v1/radar/images"
    headers = {
        "User-Agent" : "Dalvik/2.1.0 (Linux; U; Android 8.1.0; MI 5X MIUI/V10.2.3.0.ODBCNXM)",
        "Host" : "api.caiyunapp.com",
        "Connection" : "Keep-Alive",
        "Accept-Encoding" : "gzip"
    }
    params = {
        "lon" : lon, # 118.081
        "lat" : lat, # 24.48176
        "token" : "Y2FpeXVuIGFuZHJpb2QgYXBp",
        "level" : 1,
        "device_id" : "99001113012363"
    }
    r = requests.get(home, params=params, headers=headers)
    print "\t[请求网页]%s" % str(r.url).encode("utf8")
    json_str = r.text
    ret = json.loads(json_str)
    if "images" not in ret: #该地区没有imgs
        return None
    imgs = ret["images"]
    for image in imgs:
        image[1] = timestamp_to_time(image[1]) # 转换时间

    print "\t\t[imgs] %s" % str(imgs)
    return imgs


def init_crawler(params, logger):
    """ 初始化爬取工作
    :param params:
    :return:
    """
    # 四个角坐标
    nepoint = params["north_east_point"]
    # sepoint = params["south_east_point"]
    swpoint = params["south_west_point"]
    # nwpoint = params["north_west_point"]
    # 边界
    s_boundary, w_boundary = swpoint
    n_boundary, e_boundary = nepoint
    s_boundary = int(s_boundary)
    w_boundary = int(w_boundary)
    n_boundary = int(n_boundary + 0.5)
    e_boundary = int(e_boundary + 0.5)
    print s_boundary
    print w_boundary
    print n_boundary
    print e_boundary

    # 按1°分为一个图幅
    row = 0
    for x in range(s_boundary, n_boundary, 1):
        col = 0
        for y in range(w_boundary, e_boundary, 1):
            sheet_num = str(row) + ',' + str(col)
            value = {}
            value["request_points"] = (x,y)
            imgs = do_get(x, y)
            # 如果图幅正常，而且有范围exetent
            if imgs!=None and len(imgs)>0 and len(imgs[0])>=3:
                value["extent"] = imgs[0][2]
            else:
                value["extent"] = None
            request_points[sheet_num] = value
            col+=1
        row+=1
    save_path = save_json(params["out_dir"], u"1度为步长的centerpoint与extent", request_points)
    info = u"1度为步长的centerpoint与extent：{}".format(save_path)
    logger.info(info)

    # 根据extent将请求点去重
    prior_extent = None
    for key,value in request_points.items():
        if prior_extent is None:
            prior_extent = value["extent"]
            continue
        else:
            now_extent = value["extent"]
            if prior_extent == now_extent:
                request_points.pop(key)
            else:
                prior_extent = now_extent

    print "\t[每次爬取的中心点坐标] %s" % str(request_points)
    save_path = save_json(params["out_dir"], u"每次爬取的中心点坐标", request_points)
    info = u"每次爬取的中心点坐标：{}".format(save_path)
    logger.info(info)

    info = "【进程】每次需要爬取{}张图片".format( len(request_points) )
    print info
    logger.info(info)
    return request_points


if __name__ == '__main__':

    pass
