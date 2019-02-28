## 源码注释

【源码注释】
```python
# yield将Request交给scrapy的下载器->下载完成后，调用parse(self, response)函数
yield self.mark_requests_from_url(url) 
def mark_requests_from_url(self, url):
	return Request(url, dont_filter=True)
```