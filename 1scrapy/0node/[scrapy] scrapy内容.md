
【将新的url交给scrapy，继续下载】

```python
from scrapy.http import Request
from urllib ipmort parse #Python3（Python2：import urlparse）
# 【处理新得的url】构造出Request，然后通过yield交给scrap处理
yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
	# 【yield】yield交给scrapy，进行下载
	# 【url】post_url可能没有域名，其域名是当前url下的，可以使用parse.urljoin进行连接
# 【函数介绍】拼接url
parse.urljoin(base, url, allow_fragments=True)
	# base：任意一个url地址（函数会将它的主域名提取出，与url进行拼接）
	# url：如果url没有域名，就把base中的域名提取出来join进去；如果url有域名，就不join
	# 【优势】许多网站把图片放到第三方的服务器进行管理 --> 第三方服务器就涉及到跨域问题 --> parse.urljoin能够避开这个问题（看上一行url参数的说明）
```

# items
【数据爬取】从非结构性的数据源爬取到结构性的数据
【items】对爬取的目标内容进行结构化管理
【示例】对爬取JobBole.com文章的目标内容进行结构化管理（其实就是一个对象的数据结构，可以说是一个JavaBean）
```python
# items.py文件：
class JobBoleArticleItem(scrapy.Item): #文章类
	title = scrapy.Field() #标题
	create_data = scrapy.Field() #创建时间
	url = scrapy.Field() #所在url
	url_object_id = scrapy.Field() #url是变长的变量，对url进行md5变成定长
	front_image_url = scrapy.Field() #封面图
	front_image_path = scrapy.Field() #封面图已经在本地下好，记录下本地的地址
	praise_nums = scrapy.Field() #点赞数
	comment_nums = scrapy.Field() #评论数
	fav_nums = scrapy.Field() #收藏数
	tags = scrapy.Field() #标签
	content = scrapy.Field() #文章内容
```

# spider类
```
from ArticleSpider.items import JobBoleArticleItem #引入items
def parse_detail(self, response): #解析文章内容
	# 首先使用css或xpath从response中解析中数据
	title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")	
	front_image_url = response.meta.get("front_image_url", "")
	article_item = JobBoleArticleItem() #实例化一个
	# 填充JobBoleArticleItem类对应的值
	article_item["title"] = title #可以像字典一样传值
	article_item["front_image_url"] = [ front_image_url ] # scrapy的图片下载pipeline接受的是一个数组
	
	# 填充完成之后，交给scrapy，它会流向pipeline进行处理
	yield article_item
	
```

# pipeline
【pipeline】将填充完的item变量，进行处理（去重或保存）
【注册pipeline】在settings.py中配置
```
# scrapy数据流通的管道
ITEM_PIPELINES ={ # map是指存放数据的处理类
	# "类的位置" : 权重大小（数值越小，就越早进入这个pipeline）
	"scrapy.pipelines.images.ImagesPipeline" : 1, #下载图片的pipelines（自动下载图片）
	`ArticleSpider.pipelines.ArticlespiderPipeline` : 300,
}

# 【scrapy自动下载图片】scrapy提供了一个自动下载图片的机制，需要安装pillow库
IMAGES_URLS_FIELD = "front_image_url" # 配置ImagePipeline要下载的字段
	#当item流入ImagesPipeline后，它就会取出front_image_url字段，进行下载
# 配置图片保存路径
project_dir = os.path.abspath( os.path.dirname(__file__) ) # settings.py的相对路径
IMAGES_STORE = os.path.join(project_dir, "images") # 拼接路径
```



