1. scrapy默认会读取网站的robots协议，若url不遵守该协议，会被过滤掉
【解决】打开setting.py文件，找到语句`ROBOTSTXT_OBEY = False #关闭过滤`