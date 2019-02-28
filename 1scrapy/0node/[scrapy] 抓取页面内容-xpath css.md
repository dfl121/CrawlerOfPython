@[toc]
# 常用方法
## css
```
::text  //提取出文本
::attr(href) //属性有href
```

## xpath

```xpath
# text()获取文本内容
"/..../text()"  #获得文本内容
# contains(属性，属性值) 包含
"//span[ contains(@class, 'vote-post-up') ]" #class中包含了vote-post-up的span
```

## python
```python
# 【使用xpath】
response.xpath(xpath的字符串) #进行xpath提取元素，返回selector

# 【selector】
re_selector.extract() #提取data，返回list
	# 对selector进行extract操作之后就变成了数组，不能再二次提取了
re_selector.extract_first("") #提取data的第一个，如果没有取到，返回函数的第一个参数""(空)

# 【list】
tag_list = [element for element in tag_list if not element.strip().endwith("评论")] 
	#去除list中以"评论"为结尾的元素
	
# 【string】
string.strip() #去掉空格
string.replace(目标字符, 替换字符) #替换字符
tags = ",".join(tag_list)
	#将list用","连接成一个字符串
```

# css

## css选择器

|表达式|说明|
|-|-|
|`*` | 所有节点|
|`#container`|id为container的节点|
|`.container`|class包含container的节点|
|`li a`|li下的所有a节点|
|`ul + p` | ul后面的第一个p元素|
|`div#container > ul`| id为container的div的第一个ul子元素|
|`ul ~ p ` | 与ul相邻的所有p元素|
|`a[title]` | 所有有title属性的a元素|
|`a[href="http://jobbole.com"]` | 所有属性为jobbole.com值的a元素|
|`a[href*="jobole"]` | 所有href属性包含jobbole的a元素|
|`a[href^="http"]` | 所有href属性值以http开头的a元素|
|`a[href$=".jpg"]` | 所有href属性值以.jpg结尾的a元素|
|`input[type=radio]:checked` | 选中的radio的元素|
|`div:not(#container)`|id非container的div属性|
|`li:nth-child(3)`|第三个li元素|
|`tr:nth-child(2n)`|偶数个tr|

## 举例
```python
# 【网址】http://blog.jobbole.com/all-posts/
post_nodes = response.css("#archive .floated-thumb .post-thumb a")
for post_node in post_nodes:
    image_url = post_node.css("img::attr(src)").extract_first("")
    post_url = post_node.css("::attr(href)").extract_first("")
    yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

# 【网址】http://blog.jobbole.com/114641/
#提取下一页并交给scrapy进行下载
next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
if next_url:
    yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()
praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
match_re = re.match(".*?(\d+).*", fav_nums)
if match_re:
    fav_nums = match_re.group(1)

comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
match_re = re.match(".*?(\d+).*", comment_nums)
if match_re:
    comment_nums = match_re.group(1)

content = response.xpath("//div[@class='entry']").extract()[0]

tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
tags = ",".join(tag_list)
```

# xpath
【xpath】
1. xpath使用路径表达式在xml和html中进行导航
2. xpath包含标准函数库
3. xpath是一个w3c的标准

## 语法
【语法】

|表达式|说明|
|-|-|
|`article`| 选取所有article元素的所有子节点|
|`/article`|选取根元素article|
|`article/a`|选取所有属于article的子元素的a元素|
| `//div`|选取所有div子元素（无论出现在文档任何地方）|
|`article//div`|选取所有属于article元素的后代的div元素，不管它出现在article之下的任何位置|
|`//@class`|选取所有名为class的属性|
|`/div/*` | div的所有子节点|
|`//*` | 所有元素 |
|`//div[@*]` | 所有带属性的title元素|
|`/div/a | //div/p` | 所有div元素的a和p元素|
|`//span | //ul` | 文档中的span和ul元素|
|`article/div/p | //span` | article的div元素的p元素 以及 所有span元素 |

【语法-谓语】

|表达式|说明|
|-|-|
|`/article/div[1]`|选取属于article子元素的第一个div元素|
|`article/div[last() ]`|选取属于article子元素的最后一个div元素|
|`article/div[last()-1 ]` | 选取属于article子元素的倒数第二个div元素|
|`//div[@lang]` | 选取所有拥有lang属性的div元素|
|`//div[@lang='eng']` | 选取所有lang属性为eng的div元素 |

## 示例
```python
# 【网址】http://blog.jobbole.com/114641/
title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()
praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
match_re = re.match(".*?(\d+).*", fav_nums)
if match_re:
    fav_nums = match_re.group(1)

comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
match_re = re.match(".*?(\d+).*", comment_nums)
if match_re:
    comment_nums = match_re.group(1)

content = response.xpath("//div[@class='entry']").extract()[0]

tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
tags = ",".join(tag_list)
```


# 错误合集

【错误合集】

1. 根据xpath获取得到的内容错误
【原因】scrapy获取的request是网页的源码；但浏览器中查看的代码是浏览器解析后（运行js之后）的代码
【解决】尽量用id、class等方式进行定位
```python
# 示例爬取网址
start_urls = ['blog.jobbole.com/110287"] 
# 爬取成功的回调函数
def parse(self, response):
	# 在火狐浏览器中复制出的xpath：选择失败，结果为空
	re_selector = response.xpath( "/html/body/div[3]/div[3]/div[1]/div[1]/h1" )
	# 在chrome中复制出的xpath：选择成功
	re_selector = response.xpath( '//*[@id="post-110287"]/div[1]/h1' )
		## 【错误原因】在浏览器中打开的源码，是浏览器中解析之后，运行js之后的；而我们所得的response只是一个HTTP的请求，没有运行js的。所以，它们可能是不一样的。
	pass
```

# 在scrapy中使用xpath、css

【在scrapy中使用xpath、css】
1. 使用`scrapy shell 网址`来调试代码，成功后加入parse()函数中进行处理
2. 使用
```python
# 示例爬取网址
start_urls = ['blog.jobbole.com/110287"] 
# 爬取成功的回调函数
def parse(self, response):
	re_selector = response.xpath( '//*[@id="post-110287"]/div[1]/h1' )
	re_selector.extract()[0] #提取selector中的data
	pass
```