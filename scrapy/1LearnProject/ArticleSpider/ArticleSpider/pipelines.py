# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline #【scrapy自动下载图片】scrapy提供了一个自动下载图片的机制，需要安装pillow库

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