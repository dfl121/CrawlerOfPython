# -*- coding: utf-8 -*-
# 模拟知乎登录
# 慕课网scrapy教程中版本
# 大概时间为2016年
__author__ = 'bobby'

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

# 【session】代表的是某一次连接，就不需要每次都模拟登陆
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
    #session.cookies.save()是不能直接用的
    #但是cookielib.LWPCookieJar()这个类中是又save()这个方法的

# 加载cookie
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("cookie未能加载，请先登录")

# 浏览器代理
agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
# 【请求头】向服务器请求时，带给服务器的参数
header = {
    "HOST":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent
}

def is_login():
    #通过【个人中心页面】返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/question/56250357/answer/148534773"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
        # allow_redirects允许重定向
    with open("is_login.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print ("打开is_login.html查看是否登录")
    if response.status_code != 200:
        print ("未登录 " + str(response.status_code))
        return False
    else:
        print("已登录" + str(response.status_code))
        return True

#获取xsrf code
def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header) #请求一个主页
    # response = requests.get("https://www.zhihu.com") #【错误】返回500错误：request中user-agent设置的是python2/python3，不是浏览器
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text) #获取_xsrf
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


# 得到首页，查看是否登录成功
def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("zhihu_index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print ("ok")

# 得到验证码
def get_captcha():
    print("需要填写验证码")
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg","wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open('captcha.jpg') #取出验证码
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>") #输入验证码
    return captcha

# 知乎登录-手机号码登录
def zhihu_login(account, password):
    xsrf = get_xsrf()
    if xsrf=="":
        return "获取xsrf错误"
    if re.match("^1\d{10}", account):
        print ("模拟手机号码登录")
        post_url = "https://www.zhihu.com/signin"
        post_data = {
            "_xsrf": xsrf,
            "phone_num": account,
            "password": password,
            "captcha" : get_captcha() # 如果返回验证码，调用这个函数
        }
        # 模拟登陆
        response_text = session.post(post_url, data=post_data, headers=header)
        # 保存到本地cookie
        session.cookies.save()


# 测试
if __name__ == '__main__':
    ret = zhihu_login("username", "password") #登录
    print("登录 "+ str(ret) )
    get_index() # 【检查是否登录】得到首页，查看是否成功登录
    is_login() #【检查是否登录】

    # get_captcha()