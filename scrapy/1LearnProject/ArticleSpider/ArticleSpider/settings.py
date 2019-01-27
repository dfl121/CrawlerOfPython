# -*- coding: utf-8 -*-

# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArticleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines scrapy数据流通的管道
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = { # ITEM_PIPELINES存放数据的处理类
    # "类的位置" : 权重大小（数值越小，就越早进入这个pipeline）

    # ######## 其他
    'ArticleSpider.pipelines.ArticlespiderPipeline' : 300, #默认

    # ########下载图片
    # 'scrapy.pipelines.images.ImagesPipeline': 1, #下载图片的pipelines（自动下载图片）
    'ArticleSpider.pipelines.ArticleImagePipeline': 1, #下载图片的pipelines（自动下载图片）：继承ImagesPipeline，自定义函数，得到下载图像的结果

    # #######保存成JSON文件
    # 'ArticleSpider.pipelines.JsonWithEncodingPipeline' : 2, #自定义
    # 'ArticleSpider.pipelines.JsonExporterPipeline' : 2, #使用scrapy导出模块

    # #######mysql的pipeline
    # 'ArticleSpider.pipelines.MySQLPipeline' : 2, #自定义
    'ArticleSpider.pipelines.MysqlTwistedPipeline' : 2, #使用scrapy异步插入
}

# ############【scrapy自动下载图片】scrapy提供了一个自动下载图片的机制，需要安装pillow库
IMAGES_URLS_FIELD = "front_image_url" # 配置ImagePipeline要下载的字段
	#当item流入ImagesPipeline后，它就会取出front_image_url字段，进行下载
# 配置图片保存路径
project_dir = os.path.abspath(os.path.dirname(__file__)) # settings.py的相对路径
IMAGES_STORE = os.path.join(project_dir, 'images') # 拼接路径
# IMAGES_MIN_HEIGHT = 100 # 下载图像的最小高度
# IMAGES_MIN_WIDTH = 100 # 下载图像的最小宽度

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MYSQL_HOST = "47.75.49.116"
MYSQL_USER = 'consumer'
MYSQL_PASSWORD = "123456"
MYSQL_DBNAME = 'article_spider'
