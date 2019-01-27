# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.http import Request
from urllib import parse
import datetime

from ArticleSpider.items import JobBoleArticleItem #引入items
from ArticleSpider.utils.common import get_md5 #md5函数


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        """

        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("") #图片的url
            post_url = post_node.css("::attr(href)").extract_first("") #文章的url
            # 图片的url可能涉及到跨域，需要在构建request时，通过meta进行传递图片的url
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
            '''学习
            【yield】yield交给scrapy，进行下载
            【url】post_url可能没有域名，其域名是当前url下的，可以使用parse.urljoin进行连接
            【函数介绍】拼接url
                parse.urljoin(base, url, allow_fragments=True)
                    base：任意一个url地址（函数会将它的主域名提取出，与url进行拼接）
                    url：如果url没有域名，就把base中的域名提取出来join进去；如果url有域名，就不join
                    【优势】许多网站把图片放到第三方的服务器进行管理 --> 第三方服务器就涉及到跨域问题 --> parse.urljoin能够避开这个问题（看上一行url参数的说明）
            '''


    def parse_detail(self, response):  # 解析文章内容
        article_item = JobBoleArticleItem()  # 实例化一个

        # 首先使用css或xpath从response中解析中数据
        front_image_url = response.meta.get("front_image_url", "")  #文章封面图
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        content = response.css("div.entry").extract()[0]

        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        # 【加入item】
        article_item["url_object_id"] = get_md5(response.url) # url是变长的变量，对url进行md5变成定长
        article_item["title"] = title # 填充JobBoleArticleItem类对应的值
        article_item["url"] = response.url
        # [日期处理] 数据库中create_date字段是date，这里也要先进行处理
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e: #出错
            create_date = datetime.datetime.now().date() #默认为当前的日期
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url] # scrapy的图片下载pipeline接受的是一个数组
        article_item["praise_nums"] = int(praise_nums)
        article_item["comment_nums"] = int(comment_nums)
        article_item["fav_nums"] = int(fav_nums)
        article_item["tags"] = tags
        article_item["content"] = content

        # 填充完成之后，交给scrapy，它会流向pipeline进行处理
        yield article_item
