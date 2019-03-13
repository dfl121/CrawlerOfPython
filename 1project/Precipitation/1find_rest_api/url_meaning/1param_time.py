# coding:utf8
# 将目录下的json文件中的时间戳 -> 时间

import time
import json
import os

def timestamp_to_time(c):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c) )

workspace = os.path.abspath(os.curdir)#获取当前工作目录路径
print( workspace )

files = os.listdir(workspace)
for file in files:
    if not file.endswith('.json'):
        continue
    filename = file.split('.')[0]
    txtfile = filename + '.txt'
    if not os.path.exists(txtfile):
        with open(file, 'r') as load_f:
            with open(txtfile, 'w+') as f:
                dict = json.load(load_f)
                print(dict)
                images = dict["images"]
                for image in images:
                    url = image[0]
                    t = image[1]
                    extent = image[2]
                    f.write(timestamp_to_time(t) + '\n')
                f.close()
            load_f.close()