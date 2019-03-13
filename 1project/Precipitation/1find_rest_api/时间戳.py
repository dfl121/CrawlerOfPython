# coding:utf8
import time

# #################### 测试
# 获得当前时间戳
print(time.time() )

# 时间 -> 时间戳
t = "2019-03-06 10:05:00" #时间
c = time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S")) #构造时间戳
print(c) #时间戳

# 时间戳 -> 时间
c = 1551831641.0
t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c) )
print(t )

# ##################### 封装
def time_to_timestamp(t):
    return time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S"))

def timestamp_to_time(c):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c) )