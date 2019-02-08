[toc]

# Selenium
【官方文档】https://selenium-python.readthedocs.io/

【Selenium】浏览器自动化测试工具，直接运行在浏览器中，就像真正的用户在操作一样
【优势】相比于cookie、session登录方式，selenium登录是模拟人工登录时的动作，模拟登录时的分析工作较小，较简单

## 使用要求
1. 安装包 `pip install selenium`
2. 下载后把驱动文件加入环境变量。或者直接把驱动文件和 Python脚本放到同一文件夹下面
【建议firefox】相对于chrome来说，firefox没有版本限制，不容易出错
【下载网址】https://selenium-python.readthedocs.io/installation.html#drivers

【测试代码】
```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
time.sleep(5) 
driver.quit()
```

## 基础使用
### 常规

```python
webdriver.Firefox() #获取firefox浏览器驱动
元素.click() #模拟网页的某个控件的点击事件
元素.clear() #清除元素的值
元素.send_keys(username) #给元素复制
```

### 元素定位
```python
driver.find_element_by_id("id")
driver.find_element_by_name("name")
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text #通过部分超连接文本定位
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
```

### 窗口切换
```python
driver.switch_to_window('windowname') #切换window
driver.switch_to_frame('framename') #切换frame
```

### 弹窗处理
```python
alert = driver.switch_to_alert()
alert.dismiss
```

## Cookies
```python
driver.get_cookies()
jsonCookies = json.dumps(cookie)

```


# 模拟知乎登录
## 2018/1/29版本
```python
# coding=utf-8

import os
from selenium import webdriver

#知乎的用户名和密码
username = "XXXXXXX"
password = "XXX"

#，获取浏览器的驱动，这里需要提前给firefox指定环境变量，如果没有指定则需要指定路径
driver = webdriver.Firefox()

#窗口最大化
driver.maximize_window()

#打开登录页面
driver.get("https://www.zhihu.com/signup?next=%2F")

#切换到登录页面
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()

#给输入框赋值
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys(username)
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys(password)

#模拟点击事件
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()

print driver.title
os.system("pause")
```

# 相关文章
1. 【方法介绍】https://www.cnblogs.com/zhaof/p/6953241.html