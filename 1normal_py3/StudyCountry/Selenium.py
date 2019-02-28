# coding:utf8
import time
import re
from lxml import etree
from selenium import webdriver

def login():
    driver.get(home)
    target = driver.find_element_by_id('ddlogin')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    input("扫描完成后，请输入任意键")

def get_score():
    url = 'https://pc.xuexi.cn/points/my-points.html'
    # 打开新窗口
    newwindow = 'window.open("%s");' % format(url)
    driver.execute_script(newwindow)
    # 切换窗口（虽然已经调到了新窗口，但driver还是再原页面）
    handles = driver.window_handles
    driver.switch_to_window(handles[-1])  # 切换到新窗口
    # 解析网页
    html = driver.page_source
    tree = etree.HTML(html)
    # 获取总积分
    points = tree.cssselect(".my-points-points")
    total_points_str = points[0].text
    total_points = int(total_points_str)
    # 获取今日得分
    today_points_str = points[1].text
    today_points = int(today_points_str)
    # 每一项得分
    cards = tree.cssselect(".my-points-card")
    for card in cards:
        title = card.cssselect(".my-points-card-title")[0].text #标题
        score_str = card.cssselect(".my-points-card-text")[0].text #得分情况
        scores[title] = score_str

    print(total_points)
    print(today_points)
    print(scores)
    return (total_points, today_points, scores)

def do_homework(score_name):
    if score_name == u'阅读文章':
        read_article()
    elif score_name == u'观看视频':
        watch_video()
    elif score_name == u'文章学习时长':
        read_article_high()
    elif score_name == u'视频学习时长':
        read_article_high()
    pass

def read_article():
    print("正在阅读文章...")

    pass

def watch_video():
    print("正在看视频...")
    pass

def read_article_high():
    print("正在长时间阅读文章...")
    pass

def read_article_high():
    print("正在看完整视频...")
    pass

def save_html(filename):
    html = driver.page_source
    with open(filename+'.html','wb') as f:
        f.write(html)


home = 'https://pc.xuexi.cn/points/login.html?ref=https://pc.xuexi.cn/points/my-study.html'
scores = {}  # 得分情况
today_points = 0
total_points = 0
if __name__ == '__main__':
    # driver = webdriver.Chrome(executable_path='D:\mycode\CrawlerForPython\9package\phantomjs-1.9.7-windows\phantomjs.exe')
    driver = webdriver.Chrome(executable_path='D:\mycode\CrawlerForPython\9package\chromedriver.exe')
    login()
    get_score()
    while today_points<30:
        print("您的分还不够哦！%d" % today_points)
        for score_name in scores:
            score_str = scores[score_name]
            result = re.match("([0-9]+)分/([0-9]+)分", score_str)
            score = int(result.group(1))
            total = int(result.group(2))
            if score<=total:
                do_homework(score_name, score, total)

        get_score() # 刷新得分