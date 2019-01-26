# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


# 【数据爬取】从非结构性的数据源爬取到结构性的数据
# 【items】对爬取的目标内容进行结构化管理

import scrapy


class JobBoleArticleItem(scrapy.Item): #文章类
    title = scrapy.Field()  # 标题
    create_date = scrapy.Field()  # 创建时间
    url = scrapy.Field()  # 所在url
    url_object_id = scrapy.Field()  # url是变长的变量，对url进行md5变成定长
    front_image_url = scrapy.Field()  # 封面图
    front_image_path = scrapy.Field()  # 封面图已经在本地下好，记录下本地的地址
    praise_nums = scrapy.Field()  # 点赞数
    comment_nums = scrapy.Field()  # 评论数
    fav_nums = scrapy.Field()  # 收藏数
    tags = scrapy.Field()  # 标签
    content = scrapy.Field()  # 文章内容
