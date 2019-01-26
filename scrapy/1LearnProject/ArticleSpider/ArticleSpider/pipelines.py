# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline #【scrapy自动下载图片】scrapy提供了一个自动下载图片的机制，需要安装pillow库
import codecs # 【优势】避免很多编码的复杂工作
import json


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

# 保存JSON文件
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


