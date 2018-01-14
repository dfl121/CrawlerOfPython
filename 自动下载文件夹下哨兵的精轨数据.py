# -*- coding:utf-8 -*-
# Author:PasserQi
# Time:2018-1-13
# 下载文件夹下哨兵数据的精轨数据
# 须知：文件夹下的哨兵数据需解压。不想解压可以修改程序的第43行，.SAFE该为.zip
import urllib
from bs4 import BeautifulSoup
import re
import os
import datetime
import time

# 需要修改的参数
dir_path = r'G:\Sentinel-original data\Orbit40-path40\Frame75-11\added_20180105\SourceData' # 哨兵数据存在的目录
out_path = r'G:\Sentinel-original data\Orbit40-path40\Frame75-11\added_20180105\SourceData\orbit_data\tmp' #精轨数据存在的目录



error_url = []
url_prefix = 'https://qc.sentinel1.eo.esa.int/aux_poeorb/' #下载地址
def download(dest_dir, url):
    print url
    try:
        urllib.urlretrieve(url, dest_dir)
    except:
        error_url.append(url)
        print '\tError retrieving the URL:', dest_dir
    else: # 没有异常
        if url in error_url: #在错误列表里
            error_url.remove(url)

def get_yestoday(mytime):
    myday = datetime.datetime( int(mytime[0:4]),int(mytime[4:6]),int(mytime[6:8]) )
    delta = datetime.timedelta(days=-1)
    my_yestoday = myday + delta
    my_yes_time = my_yestoday.strftime('%Y%m%d')
    return my_yes_time

if __name__ == '__main__':
    # 遍历文件夹
    files = os.listdir(dir_path)
    for file in files:
        if file.endswith(".SAFE"):
            # ###########################
            # 按文件名上的信息查找EOF

            # 拼接URL
            url_param_json = {}
            url_param_json['mission'] = file[0:3]
            date = re.findall(r"\d{8}",file)[0]

            # 若参数为20170316，则搜索的是20170317的数据
            # 所以参数应该提前一天
            # 求date的前一天
            date = get_yestoday(date)

            # 在字符串指定位置插入指定字符
            # 例：20170101 --> 2017-01-01
            tmp = list(date)
            tmp.insert(4,'-');tmp.insert(7,'-')
            date = "".join(tmp)
            url_param_json['validity_start_time'] = date

            # 获得EOF下载网址
            url_param = urllib.urlencode(url_param_json) #url参数
            url = 'https://qc.sentinel1.eo.esa.int/aux_poeorb/?%s' % url_param #拼接
            html = urllib.urlopen(url)  # 获取html
            dom = BeautifulSoup(html) # 解析html文档
            a_list = dom.findAll("a")  # 找出<a>
            eof_lists = [a['href'] for a in a_list if a['href'].endswith('.EOF')]  # 找出EOF
            for eof in eof_lists:
                savefile = os.path.join(out_path,eof)
                download(savefile,url_prefix+eof)

    print "------------------------------------"
    print "开始下载出错的数据"
    # 下载出错的数据重新下载
    while len(error_url)!=0:
        print "出错的数据有"
        print error_url
        for eof in error_url:
            savefile = os.path.join(out_path, eof)
            download(savefile, url_prefix + eof)

    print "全部下载成功，无出错文件"
