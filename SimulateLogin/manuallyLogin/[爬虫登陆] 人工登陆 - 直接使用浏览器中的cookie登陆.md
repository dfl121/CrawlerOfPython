> [模拟登陆 - 0 原理]()中已经阐述模拟登陆的原理是：请求时，从cookies中将相关信息(SessionId)取出交给服务器，通过服务器的登陆拦截

【方法】最简单的方法：手工使用浏览器进行登录--> 取出浏览器中cookies的值并保存下来--> 在爬虫时每一次都将cookies打包发送
如此即可通过登录验证

【缺点】cookie的生命周期很短，若爬虫的时间较长，需要频繁更换cookie


【举例】知乎登录 - 2019/2/1
1. 打开浏览器，并登录网站进行登录www.zhihu.com
2. 打开浏览器控制台--> 打开Network，刷新页面进行抓包--> 查看到请求头

3. 将cookie的值转换成python格式
	```python
	# coding:utf8
	# 将从浏览器上复制的cookie字符串转化为python的Dict
	def stringToDict(cookie):
	    itemDict = {}
	    items = cookie.split(';')
	    for item in items:
	        key = item.split('=')[0].replace(' ', '')
	        value = item.split('=')[1]
	        itemDict[key] = value
	    return itemDict
	# 复制你获得cookie值
	cookie = '''你复制的cookie值'''
	if __name__ == "__main__":
	    dict = stringToDict(cookie)
	    print(dict)
	```
4. 在scrapy框架中使用该cookie
	```python
	# -*- coding: utf-8 -*-
	import scrapy
	from scrapy.conf import settings #从settings文件中导入Cookie，这里也可以室友from scrapy.conf import settings.COOKIE
	# 在spider中：
	class DemoSpider(scrapy.Spider):
		name = "demo"
		#allowed_domains = ["csdn.com"]
		start_urls = ["http://write.blog.csdn.net/postlist"]
		cookie = settings['COOKIE']  # 带着Cookie向网页发请求\
		headers = {
		    'Connection': 'keep - alive',  # 保持链接状态
		    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
		}
		def start_requests(self):
		    yield scrapy.Request(url=self.start_urls[0],headers=self.headers,cookies=self.cookie)# 这里带着cookie发出请求
		
		def parse(self, response):
		    print response.body
	```