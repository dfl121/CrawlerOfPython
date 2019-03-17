# coding:utf8
# @Author:PasserQi
# @Version: v1.0.0 2019/3/17

from flask import Flask, render_template, request
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict

import os
from tools import get_time
from tools import is_timestr
from tools import get_latlng
from tools import save_params_file
from worker import start

app = Flask(__name__,
    static_url_path='' #将static路径该为/，文件正常引用
)
executor = ThreadPoolExecutor(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initparam', methods=['post'])
def initparam():
    """ 初始化参数
    """
    params = OrderedDict()

    print "【从前端获得参数】 %s" % str(request.values)
    print "【正在处理参数】"

    # 【开始时间】
    params["start_time"] = request.form.get("startTime", type=str)
    if is_timestr(params['start_time']) is False:
        params['start_time'] = get_time()
    print "\t[开始时间] %s" % params["start_time"]

    # 【结束时间】
    params["end_time"] = request.form.get("endTime", type=str)
    if is_timestr(params['end_time']) is False:
        params['end_time'] = "未设置" # 不结束
    print "\t[结束时间] %s" %params["end_time"]

    # 【时间间隔】
    params["interval"] = request.form.get("interval", type=int)
    params['step'] = params['interval'] / 5  # 步长
    print "\t[时间间隔] %d" % params["interval"]
    print "\t[保存图片的步长] %d" % params["step"]

    # 【处理点】
    points = {
        'center_point' : request.form.get("centerPoint", type=str),
        'north_west_point' : request.form.get("northWestPoint", type=str),
        'north_east_point' : request.form.get("northEastPoint", type=str),
        'south_east_point' : request.form.get("southEastPoint", type=str),
        'south_north_point' : request.form.get("southNorthPoint", type=str)
    }
    print '\t[点] %s' % str(points)
    for point_name,value in points.items():
        params[point_name] = get_latlng(
            value
        )

    # 【保存文件夹】
    params["save_file_dir"] = request.form.get("saveFileDir", type=str)
    print "\t[保存文件夹] %s" % params["save_file_dir"]
    save_dir = params["save_file_dir"]
    if not os.path.exists(save_dir):
        # 选择的文件夹不存在
        print "\t【WARNING】 选择的文件夹不存在，跳转到初始页面"
        print "【params】" + str(params)
        return redirect_index("文件夹路径不存在，请重新输入！")
    # # 【输出文件夹】
    out_dir = os.path.join(save_dir, params['start_time'])
    params['out_dir'] = out_dir
    print "\t[图像输出文件夹] %s" % params["out_dir"]
    if os.path.exists(out_dir):
        # 输出文件夹已经存在
        print "【params】" + str(params)
        return redirect_index("输出文件夹已经存在，%s<Br/>请重新输入文件夹！" % out_dir)
    os.makedirs(out_dir)


    # 保存爬取参数
    print "【params】" + str(params)
    file_str = save_params_file(params)
    html_str = file_str.replace('\n', '<br/>')

    # 开启任务，异步进程
    executor.submit(start(params) )
    return '任务在后台正在运行<br/>%s' % html_str

def start(params):
    print "【开始爬取】"
    print "【params】" + str(params)

def redirect_index(msg):
    """ 重定向到index，并且显示msg
    :param msg:
    :return:
    """
    return '''
        <html>
        <head>
            <title>CityWalker</title>
            <!-- 自动跳转-->
            <meta http-equiv="Refresh" content="5;url=http://127.0.0.1:5000/"/>
        </head>
        <body>
        %s<br/>5秒后为您自动跳转
        </body>
        </html>
    ''' % msg

if __name__ == '__main__':
    # 静态资源修改不需要重启
    app.run(debug=True)