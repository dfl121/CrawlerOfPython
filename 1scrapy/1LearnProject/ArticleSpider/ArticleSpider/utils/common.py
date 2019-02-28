# -*- coding : utf-8 -*-

import hashlib

'''
:function url是变长的变量，对url进行md5变成定长
'''
def get_md5(url):
    # print ( get_md5('http://jobbole.com') ) #错误
        # python3所有的字符都是unicode，但这个函数是不接收unicode的
    if isinstance(url , str): #如果url类型是unicode
        # python3中str就是unicode
        url = url.encode("utf-8") #转成utf-8
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# 测试
if __name__ == '__main__':
    print( get_md5('http://jobbole.com'.encode("utf-8")) ) #成功