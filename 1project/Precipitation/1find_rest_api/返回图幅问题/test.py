# coding:utf8
"""
问题：请求点(x,y)
返回的情况：
1. 返回以(x,y)为中心的图幅
2. 返回(x,y)所在的图幅
结果：第二种
"""
import requests
import json
import time
from osgeo import ogr

from ospybook.vectorplotter import VectorPlotter

TIME_FORMAT = "%Y-%m-%d %H-%M"



def do_get(lat, lon):
    """ 请求
    :param lat: 纬度
    :param lon: 经度
    :return: 本次请求的images
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
    # print "\t[请求网页]%s" % str(r.url).encode("utf8")
    json_str = r.text
    ret = json.loads(json_str)
    if "images" not in ret:
        return None
    imgs = ret["images"]
    for image in imgs:
        image[1] = timestamp_to_time(image[1]) # 转换时间

    # print "\t\t[imgs] %s" % str(imgs)
    return imgs

def timestamp_to_time(c):
    """ 时间戳转成时间
    :param c:
    :return:
    """
    return time.strftime(TIME_FORMAT, time.localtime(c) )


'''
24.497303
118.110065
'''

if __name__ == '__main__':
    # vp = VectorPlotter(False)  # 非交互模式创建
    # point = ogr.Geometry(ogr.wkbPoint)
    #
    # while (1):
    #     lat = input("输入lat：")
    #     lon = input("输入lng：")
    #
    #     lat = float(lat)
    #     lon = float(lon)
    #
    #     # 中心店
    #     point.AddPoint(lon, lat)
    #     print point
    #     vp.plot(point)
    #
    #     imgs = do_get(lat, lon)
    #     extent = imgs[0][2]
    #     print extent
    #
    #     # 范围两个点
    #     point.AddPoint(extent[1], extent[0])
    #     print point
    #     vp.plot(point)
    #
    #     point.AddPoint(extent[3], extent[2])
    #     print point
    #     vp.plot(point)
    #
    #     vp.draw()
    # pass

    l = [
        (116.407526, 39.904030), #北京
        (121.473701,31.230416), #上海
        (110.349228,20.017377), #海南
        (114.305392,30.593098), #武汉
        (97.091934,33.011674), #青海玉树
        (91.140856,29.645554), #拉萨
        (102.832891,24.880095), #昆明
        (87.616848,43.825592), #乌鲁木齐
        (126.534967,45.803775), #哈尔滨
    ]

    for i,value in enumerate(l):
        imgs = do_get(value[1], value[0])
        print "经纬度\t%s" % str(value)
        if not imgs:
            print "%s no!" % i
            continue

        extent = imgs[0][2]
        print "extent\t%s" % extent
        x1, y1, x2, y2 = extent

        print "中心点坐标\t%s %s" % ( (x1+x2)/2, (y2+y1)/2 )
        len_x = x2 - x1
        len_y = y2 - y1
        print "\t\t%s %s" % (len_x , len_y)

    pass
