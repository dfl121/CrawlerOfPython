# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/16
import time

TIME_FORMAT = "%Y-%m-%d %H-%M"
RE_TIME_FORMAT = "^(\d{4}-\d{2}-\d{2}) (\d{2}-\d{2})$"

def time_to_timestamp(t):
    """ 时间转换成时间戳
    :param t:
    :return:
    """
    return time.mktime(time.strptime(t, TIME_FORMAT))

def timestamp_to_time(c):
    """ 时间戳转成时间
    :param c:
    :return:
    """
    return time.strftime(TIME_FORMAT, time.localtime(c) )

def get_time():
    """ 得到当前时间
    :return: 格式为TIME_FORMAT的时间
    """
    c = time.time()
    t = timestamp_to_time(c)
    return t

def is_timestr(str):
    """ 检查是否为时间字符串
    :param str:
    :return:
    """
    import re
    result = re.match(RE_TIME_FORMAT, str)
    if result is None:
        return False
    d = result.group(1)
    t = result.group(2)
    return d,t

def get_latlng(latlng_str):
    """ 从latlng字符串提取经纬度
    :param latlng_str:
    :return:
    """
    import re
    result = re.match('^LatLng\((.*)\)$', latlng_str)
    if result is None:
        return False
    latlng = result.group(1)
    lat,lng = latlng.split(',')
    return float(lat),float(lng)

def save_params_file(params):
    """ 将参数输出
    :param params:
    :return:
    """
    import os
    params_name = {
        "start_time": "开始时间",
        "end_time": '结束时间',
        "interval": '时间间隔',
        "center_point": '中心点坐标',
        'north_west_point': '左上角坐标',
        'north_east_point': '右上角坐标',
        'south_east_point': '右下角坐标',
        'south_north_point': '左小角坐标',
        'out_dir': '输出文件夹'
    }
    out_path = os.path.join(
        params["out_dir"], u'爬取参数.txt'
    )
    with open(out_path, 'w+') as fp:
        for param in params.keys():
            if param in params_name.keys():
                name = params_name[param]
                value = params[param]
                fp.write('【' + str(name) + '】\t' + str(value) + '\n')
        # for key,name in params_name.items():
        #     fp.write( '[' + str(name) + ']\t' + str(params[key]) + '\n' )
        fp.close()

if __name__ == '__main__':
    print is_timestr("2019-03-16 19-52-20")
    print get_latlng('LatLng(24.485274, 118.095131)')
    pass