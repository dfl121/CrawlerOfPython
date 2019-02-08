# coding:utf8
# 【测试】
# 1. selenium是否安装
# 2. 驱动是否可用
import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
time.sleep(5)
driver.quit()