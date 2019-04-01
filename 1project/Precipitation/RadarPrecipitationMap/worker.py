# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/16


from tools import is_timestr
from tools import time_to_timestamp
from tools import get_timestamp
from tools import timestamp_to_time
from tools import save_json
from crawler import do_get
from crawler import download_file
import os

# log
from tools import get_log
global logger

# debug
from collections import OrderedDict

# ------------ 定时任务 ------------
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
sched = BlockingScheduler()
# 监听器
def listener(event):
    if event.exception:
        logger.info( "【{}任务退出】{}".format(event.job_id, event.exception.message) )
    else:
        logger.info( "【爬取任务正常运行】")
sched.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


# ------------ 全局变量 ------------
global logger
global request_points #请求的中心点坐标
global end_timestrap #结束时间戳
global project_dir
global data
data = OrderedDict()
    # {
    #     "0,0" : { #图幅名
    #         "2019-03-31 17-49-00" : { #时间
    #             "time" : "",          #时间
    #             "timestamp" : "",     #时间戳
    #             "url" : "",           #下载链接
    #             "extent" : "",        #范围
    #             "req_pnt" : "",       #该瓦片请求的点坐标
    #             "file_path" : ""      #文件的path
    #         },
    #         ...
    #     },
    #     ...
    # }

# ------------ 工作入口 ------------
def start(params, req_points):
    """ 开始工作
    :param params:
    :param request_points: dict
        key : 图幅号 例"0,0"
        value : dict
            req_pnt: (x,y) 请求点
            extent : 范围
                extent is None 该请求点没有图幅
    :return:
    """
    global logger
    logger = get_log(params["out_dir"] )
    logger.info("【进程】开始下载")

    # 工程目录
    global project_dir
    project_dir = params["out_dir"]

    # 请求的中心点坐标
    global request_points
    request_points = req_points

    # 结束时间
    global end_timestrap
    end_time = params["end_time"]
    if is_timestr(end_time):
        #设置了结束时间
        end_timestrap = time_to_timestamp(end_time) #转换为时间戳好比较时间
        end_timestrap += 1*60*60 #结束时间点上的img需要之后1h小时才能爬取
    else:
        #没有设置结束时间
        end_timestrap = None

    # 开始爬取
    loop() #立即调用一次
    sched.start() # 开始定时任务
    return

# ------------ 定时任务 ------------
@sched.scheduled_job('interval', hours=1) #1h爬一次
def loop():
    # 检查是否到时间
    global end_timestrap
    global request_points
    current_timestamp = get_timestamp()
    if end_timestrap is not None: #有设置结束时间
        if current_timestamp>end_timestrap:
            sched.shutdown()

    # 爬取工作
    global data
    for frame,value in request_points.items():
        if value["extent"] is None: #该图幅没有img
            continue
        req_pnt = value["req_pnt"]
        imgs = do_get(*req_pnt)
        if imgs is None:
            logger.error("图幅{}出错：在该位置上没有获得imgs".format(frame) )
            continue
        # 处理imgs
        for img in imgs:
            timestamp = img[1] #时间戳
            time = timestamp_to_time(timestamp) #时间
            # 加入数据
            if frame not in data:
                data[frame] = OrderedDict()
            if time not in data[frame]:
                data[frame][time] = {
                    "timestamp" : timestamp,
                    "time" : time,
                    "url" : img[0],
                    "extent" : img[2],
                    "req_pnt" : req_pnt,
                    "file_path" : ""
                }
            else:
                pass
    print data

    download()
    return


def download():
    global data
    global project_dir
    global logger

    # original文件夹
    original_dir = os.path.join(project_dir, "original")
    if os.path.exists(original_dir) is False:
        os.mkdir(original_dir)

    for frame,frame_value in data.items():
        # 图幅文件夹
        frame_dir = os.path.join(original_dir, frame)
        if os.path.exists(frame_dir) is False:
            os.mkdir(frame_dir)

        for time,time_value in frame_value.items():
            # 已下载-->退出
            if time_value["file_path"] != "":
                continue

            # 下载
            url = time_value["url"]
            fn,fp = download_file(url, frame_dir)
            if fn==None: #下载错误
                logger.error("[No Download] {}".format(url) )
                continue #退出
            else: #下载完成
                time_value["file_path"] = fp
                # 保存头文件
                hdr_fn = os.path.splitext(fn)[0] #头文件名称
                save_json(frame_dir, hdr_fn, time_value)
                logger.info("[Downloaded] {}".format(fp) )
    pass



if __name__ == '__main__':
    params = OrderedDict([('start_time', '2019-03-31 19-46-03'), ('end_time', '\xe6\x9c\xaa\xe8\xae\xbe\xe7\xbd\xae'), ('interval', 5), ('step', 1), ('center_point', (24.696934, 118.083801)), ('south_west_point', (24.319286, 117.641602)), ('north_east_point', (25.072465, 118.526001)), ('south_east_point', (24.319286, 118.526001)), ('north_west_point', (25.072465, 117.641602)), ('save_file_dir', 'D:\\mycode\\CrawlerOfPython\\1project\\Precipitation\\tmp'), ('out_dir', 'D:\\mycode\\CrawlerOfPython\\1project\\Precipitation\\tmp\\2019-03-31 19-46-03')])
    req_points = OrderedDict([('0,0', {'req_pnt': (24, 117), 'extent': [21.532796186275732, 115.14559029127062, 25.66504821372427, 119.65495970872936]}), ('0,1', {'req_pnt': (24, 118), 'extent': [22.41863778627573, 115.8097463696268, 26.550889813724268, 120.35032583037321]})])

    start(params, req_points)

    # 【结果】
    data = OrderedDict([('0,0', OrderedDict([('2019-03-31 17-49-00', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331094900_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554025740.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 17-49-00', 'file_path': ''}), ('2019-03-31 17-54-59', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331095459_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554026099.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 17-54-59', 'file_path': ''}), ('2019-03-31 18-00-59', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331100059_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554026459.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-00-59', 'file_path': ''}), ('2019-03-31 18-06-59', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331100659_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554026819.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-06-59', 'file_path': ''}), ('2019-03-31 18-12-59', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331101259_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554027179.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-12-59', 'file_path': ''}), ('2019-03-31 18-18-59', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331101859_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554027539.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-18-59', 'file_path': ''}), ('2019-03-31 18-24-59', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331102459_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554027899.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-24-59', 'file_path': ''}), ('2019-03-31 18-30-59', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331103059_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554028259.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-30-59', 'file_path': ''}), ('2019-03-31 18-36-58', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331103658_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554028618.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-36-58', 'file_path': ''}), ('2019-03-31 18-42-58', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331104258_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554028978.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-42-58', 'file_path': ''}), ('2019-03-31 18-48-57', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331104857_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554029337.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-48-57', 'file_path': ''}), ('2019-03-31 18-54-57', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331105457_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554029697.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 18-54-57', 'file_path': ''}), ('2019-03-31 19-00-57', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331110057_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554030057.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-00-57', 'file_path': ''}), ('2019-03-31 19-06-57', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331110657_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554030417.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-06-57', 'file_path': ''}), ('2019-03-31 19-12-56', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331111256_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554030776.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-12-56', 'file_path': ''}), ('2019-03-31 19-18-56', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331111856_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554031136.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-18-56', 'file_path': ''}), ('2019-03-31 19-24-55', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331112455_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554031495.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-24-55', 'file_path': ''}), ('2019-03-31 19-30-54', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331113054_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554031854.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-30-54', 'file_path': ''}), ('2019-03-31 19-36-54', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331113654_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554032214.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-36-54', 'file_path': ''}), ('2019-03-31 19-42-54', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9596_nmc_fast/20190331/Z_RADR_I_Z9596_20190331114254_P_DOR_SA_R_10_230_15.596.clean.png', 'timestamp': 1554032574.0, 'req_pnt': (24, 117), 'extent': [21.5327961863, 115.1455902913, 25.6650482137, 119.6549597087], 'time': '2019-03-31 19-42-54', 'file_path': ''})])), ('0,1', OrderedDict([('2019-03-31 17-50-16', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331095016_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554025816.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 17-50-16', 'file_path': ''}), ('2019-03-31 17-55-56', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331095556_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554026156.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 17-55-56', 'file_path': ''}), ('2019-03-31 18-01-37', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331100137_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554026497.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-01-37', 'file_path': ''}), ('2019-03-31 18-07-18', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331100718_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554026838.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-07-18', 'file_path': ''}), ('2019-03-31 18-12-58', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331101258_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554027178.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-12-58', 'file_path': ''}), ('2019-03-31 18-18-40', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331101840_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554027520.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-18-40', 'file_path': ''}), ('2019-03-31 18-24-22', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331102422_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554027862.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-24-22', 'file_path': ''}), ('2019-03-31 18-30-01', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331103001_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554028201.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-30-01', 'file_path': ''}), ('2019-03-31 18-35-43', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331103543_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554028543.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-35-43', 'file_path': ''}), ('2019-03-31 18-41-25', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331104125_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554028885.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-41-25', 'file_path': ''}), ('2019-03-31 18-47-08', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331104708_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554029228.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-47-08', 'file_path': ''}), ('2019-03-31 18-52-48', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331105248_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554029568.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-52-48', 'file_path': ''}), ('2019-03-31 18-58-30', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331105830_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554029910.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 18-58-30', 'file_path': ''}), ('2019-03-31 19-04-11', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331110411_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554030251.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 19-04-11', 'file_path': ''}), ('2019-03-31 19-09-52', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331110952_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554030592.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 19-09-52', 'file_path': ''}), ('2019-03-31 19-15-33', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331111533_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554030933.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 19-15-33', 'file_path': ''}), ('2019-03-31 19-21-15', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331112115_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554031275.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 19-21-15', 'file_path': ''}), ('2019-03-31 19-26-56', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331112656_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554031616.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 19-26-56', 'file_path': ''}), ('2019-03-31 19-32-38', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331113238_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554031958.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 19-32-38', 'file_path': ''}), ('2019-03-31 19-38-20', {'url': u'http://cdn.caiyunapp.com/res/storm_radar/radar_NMIC_AZ9592_nmc_fast/20190331/Z_RADR_I_Z9592_20190331113820_P_DOR_SA_R_10_230_15.592.clean.png', 'timestamp': 1554032300.0, 'req_pnt': (24, 118), 'extent': [22.4186377863, 115.8097463696, 26.5508898137, 120.3503258304], 'time': '2019-03-31 19-38-20', 'file_path': ''})]))])

    pass