# -*- coding: utf-8 -*-
# 【模拟知乎登录】视频版本-大概2016年
import re
import json
import datetime

try:
    import urlparse as parse
except:
    from urllib import parse

import scrapy


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"] #域名
    start_urls = ['https://www.zhihu.com/'] #开始的url
    # 请求头
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        pass

    # 重写start_request控制入口完成登录
    def start_requests(self):
        # 【使用scrapy异步ui，构造一个登录的url，并指定成功请求后的回调函数callback】
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]

    # 登录函数
    def login(self, response):
        # 【xsrf】老版本的xsrf是在html中
        # 获取xsrf
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
            # 【问题】默认是解析第一行<DOC html>的神明
            # 【解决】加上DOTALL，解析页面所有的字符
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))
        else:
            print("获取xsrf失败")

        # 获取成功
        if xsrf!="":
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "18759073625",
                "password": "qiqi730899$%.",
                "captcha": ""
            }

            import time
            t = str(int(time.time() * 1000))
            # 获取验证码的图片
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            # 构造请求图片的request
            yield scrapy.Request(captcha_url,
                headers=self.headers,
                meta={
                    "post_data":post_data
                },
                callback=self.login_after_captcha # 设置回调函数
            )


    # 获得验证码图片，并手动输入验证码
    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha
        # 构造请求表单
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login #回调函数
        )]

    def check_login(self, response):
        # 【说明】登录成功后，不需要自己保存cookie，scrapy会帮我们处理
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            # 开始爬取页面
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

