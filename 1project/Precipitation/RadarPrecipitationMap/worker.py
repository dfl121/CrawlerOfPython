# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/16

from crawler import do_get

def start(params):
    """ 开始工作
    :param params:
    :return:
    """
    print params['center_point']
    center_point = params['center_point']
    imgs = do_get(center_point[0], center_point[1])
    print imgs[0][2]
    current_extent = imgs[0][2]
    check_extent()
    pass

def check_extent(center_point, extent, current_extent):
    """ 检查范围
    :param center_point: 中心点坐标 (lat, lng)
    :param extent: 要求范围 （同current_extent）
    :param current_extent: 当前的范围 
        [左下角经纬度,右上角经纬度] eg： [22.41863778627573, 115.8097463696268, 26.550889813724268, 120.35032583037321]
    :return: req_params 每次请求的参数
        [(lat1, lng1), (lat2, lng2), .... ]
    """
    req_params = []

    return req_params


if __name__ == '__main__':
    params = {'out_dir': 'D:\\mycode\\CrawlerOfPython\\1project\\Precipitation\\tmp\\2019-03-15 19-34',
              'start_time': '2019-03-15 19-34',
              'step': 1,
              'save_file_dir': 'D:\\mycode\\CrawlerOfPython\\1project\\Precipitation\\tmp',
              'south_east_point': (24.492148, 118.129635),
              'center_point': (24.492148, 118.129635),
              'interval': 5,
              'south_north_point': (24.492148, 118.129635),
              'north_east_point': (24.492148, 118.129635),
              'end_time': '\xe6\x9c\xaa\xe8\xae\xbe\xe7\xbd\xae',
              'north_west_point': (24.492148, 118.129635)
    }
    start(params)
    pass