【背景知识】
1. phantomjs是一个基于webkit的没有界面的浏览器，所以运行起来比完整的浏览器要高效

【下载Phantomjs】https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-windows.zip

【测试】
```python
#coding=utf-8
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='C:\Users\Gentlyguitar\Desktop\phantomjs-1.9.7-windows\phantomjs.exe')
driver.get("http://duckduckgo.com/")
driver.find_element_by_id('search_form_input_homepage').send_keys("Nirvana")
driver.find_element_by_id("search_button_homepage").click()
print driver.current_url
driver.quit()
```

【链接】
1. https://www.cnblogs.com/chenqingyang/p/3772673.html?tdsourcetag=s_pctim_aiomsg