# scrapy工程文件介绍
【scrapy工程文件介绍】

- ArticleSpider
	- ArticleSpider
		- Spiders 存放具体某个网站的爬虫
			- `__init__.py` 
			- `jobbole.py` 爬虫文件，使用命令`scrapy genspider jobbole blog.jobbole.com`生成
		- `__init__.py`
		- `items.py` 数据保存格式
		- `middlewares.py` 存放自己定义的middleware
		- `pipelines.py`数据存储
		- `settings.py` 设置文件
	- `scrapy.cfg`  配置文件


# 开发scrapy步骤
1. 【创建工程与虚拟环境】创建工程与Python虚拟环境
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126095144290.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)
2. 【进入虚拟环境】进入刚才创建的Python虚拟环境
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126095503542.png)
3. 【安装scrapy】运行命令`pip install -i https://pypi.douban.com/simple/ scrapy`安装scrapy
【提示】若中途发生失败，请手动安装失败的包https://blog.csdn.net/summer_dew/article/details/79778559#pip_96

4. 【创建scrapy工程】：在当前目录下运行`scrapy startproject ArticleSpider`，新建scrapy工程（只是一个scrapy工程框架，里头没有spider的模板）
【说明】`scrapy startproject 工程名`。也可以自定义模板，默认模板："...\lib\site-packages\scrapy\templates\project"
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019012610124585.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

5. 【创建spider】进入运行`ArticleSpider\ArticleSpider\spiders`下，运行命令`scrapy genspider jobbole blog.jobbole.com`，生成spider器
【说明】`scrapy genspider spider器的名称 爬取的目标域名`，在当前目录下生成spider文件
【结果】在Spiders/目录下生成了`jobbole.py`文件
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126101559645.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

6. 【加入刚才创建的Python虚拟环境】
【步骤】`File-> setting-> Project:ArticleSpider-> Project Interpreter-> Add-> System Interpreter-> 选择D:\mycode\CrawlerForPython\scrapy\Python3Scrapy\Scripts\python.exe`

7. 【配置工程的解释器】
【步骤】`Add Configuration --> 左上方+号 --> Python`
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126102433247.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)
8. 在ArticleSpider文件夹下创建main.py文件，用于scrapy调试
【背景】 Pycharm没有scrapy的模板，实际上是没有办法调试的
【技巧】 `新建一个main.py`，在文件中调用命令行
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126102904751.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)
```python
# coding:utf-8
from scrapy.cmdline import execute
import sys
import os
# 设置工程路径
sys.path.append(
	os.path.dirname( #获取current_paths当前的文件夹目录
		os.path.abspath( __file__ ) #获取__file__(当前py文件)的绝对路径
	)
)
execute(["scrapy", "crawl", "jobbole"] ) #启动scrapy，相当于命令行scrapy crawl jobbole
```

9. 运行该main.py文件
【报错】ModuleNotFoundError: No module named 'win32api'。则还需要`pypiwin32`模块 ，进入python虚拟环境运行：`pip install -i https://pypi.douban.com/simple pypiwin32` 
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190126103142266.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)