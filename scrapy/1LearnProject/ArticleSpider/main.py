# coding:utf-8
from scrapy.cmdline import execute
import sys
import os


# 设置工程路径
sys.path.append(
	os.path.dirname( #获取current_paths当前的文件夹目录
		os.path.abspath( __file__ ) #获取__file__(当前py文件)的绝对路径
	)
)
# execute(["scrapy", "crawl", "jobbole"] ) #启动scrapy，相当于命令行scrapy crawl jobbole

execute(["scrapy", "crawl", "zhihu"]) #知乎