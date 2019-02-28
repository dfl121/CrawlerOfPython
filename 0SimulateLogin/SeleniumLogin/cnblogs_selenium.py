# coding:utf-8
import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time

#新建session
s = requests.session()
url = "https://home.cnblogs.com/u/TankXiao"

def get_cookies(url):
    u'启动selenium获取浏览器cookies'
    driver = webdriver.Firefox()
    driver.get(url+"/followers")
    driver.find_element_by_xpath('//*[@id="input1"]').send_keys("***")
    driver.find_element_by_xpath('//*[@id="input2"]').send_keys("****/")
    driver.find_element_by_xpath('//*[@id="signin"]').click()
    time.sleep(15)
    cookie = driver.get_cookies()   #获取浏览器cookies
    driver.quit()
    return cookie
def add_cookies(cookie):
    u"往session添加cookies"
    c = requests.cookies.RequestsCookieJar()
    for i in cookie:    #添加cookie到CookieJar
        c.set(i["name"], i["value"])
    s.cookies.update(c)     #更新session里的cookie
def get_ye_num(url):
    u'获取粉丝页面数量'
    r1 = s.get(url+"/relation/followers")
    soup = BeautifulSoup(r1.content,"html.parser")
    #获取粉丝数
    fans_text = soup.find_all(class_="current_nav")
    print(fans_text[0].string)
    fans_num = re.findall(u"的粉丝\((.+?)\)",fans_text[0].string)      #返回未list数据
    fans_num = int(fans_num[0])    #将fans_num从string转换为int
    #计算粉丝页数
    ye = int(fans_num/45)+1     #ye为int型
    return ye
def save_name(ye):
    u'保存粉丝名'
    text = ''
    for i in range(1, ye+1):
        r2 = s.get(url+"/relation/followers/?page=%s"%i)
        soup1 = BeautifulSoup(r2.content,"html.parser")
        fans_list = soup1.find_all(class_="avatar_name")  #查找粉丝
        for j in fans_list:     #从list中获取每个粉丝的名并添加到text
            text = text+j.string
    name = bytes(text, encoding="utf-8")    #将text转换为bytes格式
    w = open('name.txt','wb')       #打开name.txt文件为可写入
    w.write(name)       #写入
    w.close()
if __name__ == "__main__":
    cookie = get_cookies(url)
    add_cookies(cookie)
    ye = get_ye_num(url)
    save_name(ye)