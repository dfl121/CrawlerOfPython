# coding:utf8
import time
import re
from lxml import etree
from selenium import webdriver

ARTICLE_READ_TIME = 4

def login():
    home = 'https://pc.xuexi.cn/points/login.html?ref=https://pc.xuexi.cn/points/my-study.html'
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
    driver.switch_to_window(driver.window_handles[-1])  # 切换到新窗口
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
    driver.close()
    driver.switch_to_window(driver.window_handles[0])

    print(total_points)
    print(today_points)
    print(scores)
    return (total_points, today_points, scores)

def do_homework(score_name, score, total):
    start_study()
    if score_name == u'阅读文章':
        read_article(score, total, False)
    elif score_name == u'观看视频':
        watch_video(score, total)
    elif score_name == u'文章学习时长':
        read_article_high(score, total, True)
    elif score_name == u'视频学习时长':
        read_article_high(score, total)
    close_study()

def start_study():
    study_url = 'https://www.xuexi.cn/'
    # 打开新窗口
    newwindow = 'window.open("%s");' % format(study_url)
    driver.execute_script(newwindow)
    # 切换窗口（虽然已经调到了新窗口，但driver还是再原页面）
    driver.switch_to_window( driver.window_handles[-1] )  # 切换到新窗口

def close_study():
    driver.close()
    driver.switch_to_window( driver.window_handles[0] )

def read_article(score, total, flag):
    """
    :param score:
    :param total:
    :param flag: flag=True长时间浏览
    :return:
    """
    print("正在阅读文章...")
    words = driver.find_elements_by_css_selector('.word-item') #获得所有文章element
    for word in words:
        if score<total: # 分数还没有满
            word.click() #点击
            driver.switch_to_window(driver.window_handles[-1])  # 切换到新窗口
            if flag: #长时间浏览
                time.sleep(ARTICLE_READ_TIME*60)
            scroll_foot() #拉倒最底下
            driver.close()
            driver.switch_to_window(driver.window_handles[-1])  # 切换到新窗口
            score+=1
    pass

def watch_video(score, total):
    print("正在看视频...")
    pass

def read_article_high(score, total):
    print("正在长时间阅读文章...")
    pass

def scroll_foot():
    # 拉到底部
	if driver.name=="chrome":
		js = "var q = document.body.scrollTop=10000000000"
	else:
		js = "var q = document.documentElement.scrollTop=10000000000"
	driver.execute_script(js)

def save_html(filename):
    html = driver.page_source
    with open(filename+'.html','wb') as f:
        f.write(html)


scores = {}  # 得分情况
today_points = 0
total_points = 0
if __name__ == '__main__':
    # driver = webdriver.Chrome(executable_path='D:\mycode\CrawlerForPython\9package\phantomjs-1.9.7-windows\phantomjs.exe')
    driver = webdriver.Chrome(executable_path='D:\mycode\CrawlerForPython\9package\chromedriver.exe')
    login()
    total_points, today_points, scores = get_score()
    while today_points<30:
        print("今日累计%d积分" % today_points)
        for score_name in scores:
            score_str = scores[score_name]
            result = re.match("([0-9]+)分/([0-9]+)分", score_str)
            score = int(result.group(1))
            total = int(result.group(2))
            if score<=total:
                do_homework(score_name, score, total)

        total_points, today_points, scores = get_score() # 刷新得分