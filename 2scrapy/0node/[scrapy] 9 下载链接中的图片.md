# 获取文章的图片
【item类】
```python
class JobBoleArticleItem(scrapy.Item): #文章类
	front_image_url = scrapy.Field() #封面图
	front_image_path = scrapy.Field() #封面图已经在本地下好，记录下本地的地址
```

【spider类】获取图片的url
```python
# 【传递图片的url】
def parse(self, response):
	post_nodes = response.css("#archive .floated-thumb .post-thumb a")
	for post_node in post_nodes:
		image_url = post_node.css("img::attr(src)").extract_first("") #图片的url
		post_url = post_node.css("::attr(href)").extract_first("") #文章的url
		# 图片的url可能涉及到跨域，需要在构建request时，通过meta进行传递图片的url
		yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)
			
# 【取出图片的Url】
from ArticleSpider.items import JobBoleArticleItem #引入items
def parse_detail(self, response): #解析文章内容	
	front_image_url = response.meta.get("front_image_url", "")
	article_item = JobBoleArticleItem() #实例化一个
	article_item["front_image_url"] = [ front_image_url ] # scrapy的图片下载pipeline接受的是一个数组
	# 填充完成之后，交给scrapy，它会流向pipeline进行处理
	yield article_item
```

【下载】scrapy提供了一个自动下载图片的机制，需要安装pillow库
在settings.py中进行配置：
```
# scrapy数据流通的管道
ITEM_PIPELINES = { # 存放数据的处理类
	# "类的位置" : 权重大小（数值越小，就越早进入这个pipeline）
	"scrapy.pipelines.images.ImagesPipeline" : 1, #下载图片的pipelines（自动下载图片）
}
# 配置ImagePipeline要下载的字段
IMAGES_URLS_FIELD = "front_image_url" #当item流入ImagesPipeline后，它就会取出front_image_url字段，进行下载
# 配置图片保存路径
project_dir = os.path.abspath( os.path.dirname(__file__) ) # settings.py的相对路径
IMAGES_STORE = os.path.join(project_dir, "images") # 拼接路径
```