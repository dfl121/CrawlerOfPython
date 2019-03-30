# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/16

from crawler import init_crawler

# log
from tools import get_log
global logger

# debug
from collections import OrderedDict

def start(params):
    """ 开始工作
    :param params:
    :return:
    """
    logger = get_log(params["out_dir"])
    logger.info("【进程】开始下载")

    logger.info("【进程】爬取工作初始化")
    init_crawler(params, logger)

    pass





if __name__ == '__main__':
    params = OrderedDict([('start_time', '2019-03-19 20-14'), ('end_time', '\xe6\x9c\xaa\xe8\xae\xbe\xe7\xbd\xae'), ('interval', 5), ('step', 1), ('center_point', (24.497303, 118.110065)), ('south_west_point', (24.417552, 117.994537)), ('north_east_point', (24.577108, 118.225594)), ('south_east_point', (24.417552, 118.225594)), ('north_west_point', (24.577108, 117.994537)), ('save_file_dir', 'D:\\mycode\\CrawlerOfPython\\1project\\Precipitation\\tmp'), ('out_dir', 'D:\\mycode\\CrawlerOfPython\\1project\\Precipitation\\tmp\\2019-03-19 20-14')])
    start(params)

    pass