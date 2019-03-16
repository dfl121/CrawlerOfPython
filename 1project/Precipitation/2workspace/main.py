# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/16

import os
from tools import get_time
from tools import is_timestr
from tools import get_latlng
from tools import save_params_file
from worker import start

HTML = r'D:\mycode\CrawlerOfPython\1project\Precipitation\2workspace\html\index.html'
def open_html():
    import webbrowser
    webbrowser.open(HTML)

def init_param(params):
    """ 初始化参数
    :param params: key命名方式参照HTML中表单的name属性
    :return: 初始化参数
    """
    points_names = [
        'center_point',
        'north_west_point',
        'north_east_point',
        'south_east_point',
        'south_north_point'
    ]
    # 处理开始时间
    if is_timestr(params['start_time']) is False:
        params['start_time'] = get_time()
    # 处理结束时间
    if is_timestr(params['end_time']) is False:
        params['end_time'] = "未设置" # 不结束
    # 处理时间间隔
    params['interval'] = int(params['interval'])
    params['step'] = params['interval']/5 #步长
    # 处理点
    for point_name in points_names:
        params[point_name] = get_latlng(
            params[point_name]
        )
    # 创建保存文件夹
    save_dir = params["save_file_dir"]
    if not os.path.exists(save_dir):
        # 选择的文件夹不存在
        return False
    out_dir = os.path.join(save_dir, params['start_time'] ) #输出的文件夹
    params['out_dir'] = out_dir
    if os.path.exists(out_dir):
        # 输出文件夹已经存在
        return False
    os.makedirs(out_dir)
    # 输出爬取参数
    save_params_file(params)
    return params




if __name__ == '__main__':
    # 打开HTML
    # open_html()

    # 测试初始化参数
    params = {
        "start_time": "2019-03-15 19-34",
        "end_time": u'可选项（默认不自动停止）',
        "interval": u'5',
        "center_point": u'LatLng(24.492148, 118.129635)',
        'north_west_point': u'LatLng(24.492148, 118.129635)',
        'north_east_point': u'LatLng(24.492148, 118.129635)',
        'south_east_point': u'LatLng(24.492148, 118.129635)',
        'south_north_point': u'LatLng(24.492148, 118.129635)',
        'save_file_dir': r'D:\mycode\CrawlerOfPython\1project\Precipitation\tmp'
    }
    print init_param(params)