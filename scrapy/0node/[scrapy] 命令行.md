## scrapy命令行
【启动scrapy工程】
`scrapy crawl jobbole #启动scrapy`

【调试url】
```bash
scrapy shell https://blog.jobbole.com/110287/
# 运行上行命令后，可以进行一些调试操作，例如xpath相关操作
>>> title = response.xpath("//div[@class='entry-header']/h1/text()")
>>> title.extract() #提取Selector中的data
```

【注意】
1. 在scrapy下使用不了很多的Python逻辑，需要调试python代码，可以进入cmd的ipython环境

# 错误合集

【问题1】`ImportError: No module named 'win32api'`
【解决】`> pip install -i https://pypi.douban.com/simple pypiwin32 #安装`


【问题2】`Unknown command: crawl 或 Scrapy-no active project `
【解决】https://blog.csdn.net/godot06/article/details/81558910