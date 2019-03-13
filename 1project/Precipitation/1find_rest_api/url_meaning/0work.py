# coding:utf8
# 【背景】因为url没有时间参数 --> 猜测：url返回某个时间点（请求时间）前4个小时内的瓦片
# 【测试】分多个时间点，测试同一个Url，查看是否有变化
# 【url】https://api.caiyunapp.com/v1/radar/images?lon=118.089561&lat=24.48176&token=Y2FpeXVuIGFuZHJpb2QgYXBp&level=1&device_id=99001113012363
import requests
import time
import datetime

url = 'https://api.caiyunapp.com/v1/radar/images?lon=118.089561&lat=24.48176&token=Y2FpeXVuIGFuZHJpb2QgYXBp&level=1&device_id=99001113012363'

header = {
    'User-Agent' : 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; MI 5X MIUI/V10.2.3.0.ODBCNXM)',
    'Accept-Encoding' : 'gzip'
}

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
def work():
    r = requests.get(url, headers=header)
    nowTime = get_time()
    with open(nowTime+'.json', 'w+') as f:
        f.write(r.text)
        print("[OK]  " + str(nowTime) )
        f.close()

if __name__ == '__main__':
    print( get_time() )
    while (True):
        get_time()
        work()
        time.sleep(30 * 60)