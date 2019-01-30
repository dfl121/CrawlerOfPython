# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


# 【数据爬取】从非结构性的数据源爬取到结构性的数据
# 【items】对爬取的目标内容进行结构化管理

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

import datetime
import re


# ################ 将Item值进行预处理
def add_jobbole(value):
    return value + "-bobby"
def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums
def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value
def return_value(value):
    return value
# 【Item】文章类Item
class JobBoleArticleItem(scrapy.Item):
    # 将传递进来的值进行预处理，可以传递多个处理函数
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
        # output_processor=TakeFirst()  # 只取第一个
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    # front_image_url是要交给scrapy自动下载图片的pipeline，其要求的是一个list
    # 默认的ItemLoader是将所有的成员都变成list
    # 但经过自定义的ArticleItemLoader之后，它变成了一个字符串，不是list
    front_image_url = scrapy.Field(
        # 所以这里需要处理一下，把ArticleItemLoader的默认default_output_processor进行覆盖掉
        output_processor = MapCompose(return_value) # 传入了一个将值进行预处理的函数
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        # input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",") #用','连接tag
    )
    content = scrapy.Field()

# 重载ItemLoader，自定义其功能
# 若只需要一个item进行取第一个，在scrapy.Field()传入的预处理函数中加上output_processor = TakeFirst() # 只取第一个
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst() #只取第一个