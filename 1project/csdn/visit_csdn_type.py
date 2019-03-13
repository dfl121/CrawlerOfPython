# coding:utf8
# py3
import requests
from lxml import etree
import re
import time

home = "https://blog.csdn.net/summer_dew/article/category/8089774/"
page_total_num = 2

class VisitCsdn(object):
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    article_urls = []

    def __init__(self, _home, _total):
        self.home = _home
        self.page_total = _total


    # def get_page_total(self):
    #     print(self.home) #debug
    #     page_nums = []
    #     r = requests.get(self.home, headers=self.headers)
    #     tree = etree.HTML(r.text)
    #     lis = tree.cssselect(".pagination-box > li")
    #     for li in lis:
    #         li_text = li.text
    #         result = re.match("[0-9]+", li_text)
    #         if result!=None:
    #             page_nums.append(
    #                 int(li_text)
    #             )
    #     print(page_nums)
    #     self.page_total = page_nums[-1]

    def get_article_url(self):
        for num in range(1, self.page_total+1):
            url = self.home + str(num)
            print(url)
            r = requests.get(url, headers=self.headers)
            html = r.text
            tree = etree.HTML(html)
            items = tree.cssselect(".article-item-box")
            for item in items:
                a = item.cssselect("a")[0]
                self.article_urls.append(
                    a.get("href")
                )

    def start_visit(self):
        # self.get_page_total()  # 获得页面总数
        self.get_article_url() # 获得页面urls
        print(self.article_urls)
        print("[开始访问]")
        print("一共有%d" % len(self.article_urls) )
        while (True):
            for url in self.article_urls:
                print(url)
                r = requests.get(url, headers=self.headers)
                time.sleep(5)
            time.sleep(15)
            print("[again]")

if __name__ == '__main__':
    obj = VisitCsdn(home, page_total_num)
    obj.start_visit()

