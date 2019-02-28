【相关文档】

1. lxml：https://lxml.de/
2. xpath：http://www.w3school.com.cn/xpath/xpath_syntax.asp

# 使用xpath、cssselect

```python
# 【方法一】HTML页面是string
tree = lxml.html.fromstring(html.decode("utf-8") )
# 【方法二】
from lxml import etree
html = driver.page_source
tree = etree.HTML(html)
```


# cssslect

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

## 基本函数与属性

```python
选出来的对象.text #获取文本
```

# xpath

【xpath】
1. xpath使用路径表达式在xml和html中进行导航
2. xpath包含标准函数库
3. xpath是一个w3c的标准

## 语法

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

# 题外话
## 正则表达式的常规使用
【链接】http://www.runoob.com/python/python-reg-expressions.html

```python
str = '1分/1分'
result = re.match("([0-9]+)分/([0-9]+)分", score_str)
score = int(result.group(1))
total = int(result.group(2))
```