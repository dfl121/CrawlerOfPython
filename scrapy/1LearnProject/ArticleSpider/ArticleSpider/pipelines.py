# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline #【scrapy自动下载图片】scrapy提供了一个自动下载图片的机制，需要安装pillow库
from scrapy.exporters import JsonItemExporter # 【scrapy自带导出模块】可以将item导出成许多文件格式
from twisted.enterprise import adbapi # 【功能】将mysqldb操作变成一些异步化的操作

import codecs # 【优势】避免很多编码的复杂工作
import json

import MySQLdb
import MySQLdb.cursors

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

# 【目的】得到scrapy下载图像的地址
# 继承scrapy.pipelines.images.ImagesPipeline，达到对其功能进行定制，重写
class ArticleImagePipeline(ImagesPipeline):
    # 重载下载完成
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"] #获取文件路径
            item["front_image_path"] = image_file_path #赋值给item

        return item #返回item给下一个pipeline

# ############### 导出JSON文件
# 【方法一】自定义json的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        # 打开json文件
        self.file = codecs.open('article_json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps( dict(item), ensure_ascii=False ) + '\n' #转换成json
            # ensure_ascii=True：写入中文或其他编码是会出错的
        self.file.write(lines)
        return item #返回item，下一个pipeline可能要处理
    # spider信号链：当spider进行close时，这个函数就会被调用
    def spider_close(self):
        self.file.close()
# 【方法二】调用scrapy提供的json export导出json文件
class JsonExporterPipeline(object):

    def __init__(self):
        self.file = open('articleexport.json', 'wb') #以二进制的方式打开
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False) #实例化一个JsonItemExporter变量
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting() #停止导出
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item) #把item传进来，进行处理
        return item #返回item，进入下一个pipeline

# ###################### 存入mysql
# 【方法一】自定义：采用同步的机制写入mysql
# 【问题】解析的速度肯定是远远快于入库的速度，就会导致pipeline的堵塞
class MySQLPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('47.75.49.116', 'consumer', "123456", 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = "insert into jobbole_article(" \
                     "title, create_date, url," \
                     "url_object_id, front_image_url, front_image_path," \
                     "comment_nums, fav_nums, praise_nums, " \
                     "tags, content) " \
                     "values (%s, %s, %s, " \
                     "%s, %s, %s, " \
                     "%s, %s, %s, " \
                     "%s, %s)"
        self.cursor.execute( insert_sql,  (
                item["title"], item["create_date"], item["url"],
                item["url_object_id"], item["front_image_url"][0], item["front_image_path"],
                item["comment_nums"], item["fav_nums"], item["praise_nums"],
                item["tags"],
                item["content"]
            )
        )
        self.conn.commit()
# 【方法二】scrapy提供一个连接池，让插入变成一种异步的操作
# 【说明】只是提供了一个异步容器，并没有提供数据库连接
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''
        :param cls: 其实就是MysqlTwistedPipeline这个类
        :param settings: from_settings方法会被sracpy调用，会将settings.py里的内容当settings参数传入
        '''

        # 从settings中获取参数
        dbparams = dict (
            # 【注意】变量名称：要与MySQLdb.connect中的参数相同
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        # 连接池
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams ) # **：变成可变化的参数
        return cls(dbpool) # 等同于MysqlTwistedPipeline(dbpool)，实例化出MysqlTwistedPipeline

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item) # 第一个参数：将要变成异步操作的函数
        query.addErrback(self.handle_error, item, spider) #添加一个错误处理函数
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入逻辑
        insert_sql = "insert into jobbole_article(" \
                     "title, create_date, url," \
                     "url_object_id, front_image_url, front_image_path," \
                     "comment_nums, fav_nums, praise_nums, " \
                     "tags, content) " \
                     "values (%s, %s, %s, " \
                     "%s, %s, %s, " \
                     "%s, %s, %s, " \
                     "%s, %s)"
        cursor.execute(insert_sql, (
                item["title"], item["create_date"], item["url"],
                item["url_object_id"], item["front_image_url"][0], item["front_image_path"],
                item["comment_nums"], item["fav_nums"], item["praise_nums"],
                item["tags"],
                item["content"]
            )
        )
# 【方法三】使用DjangoItem，可以像hibernate一样的方式进行保存（对象.save()完成保存，不用自己写sql语句）
# 【网址】https://github.com/scrapy-plugins/scrapy-djangoitem