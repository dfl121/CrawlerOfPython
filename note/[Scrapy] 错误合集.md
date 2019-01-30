【错误】ItemLoader报错
```
    item[field_name] = value
TypeError: 'ItemMeta' object does not support item assignment
```
[解决]
1. `item_loader = ItemLoader(item=JobBoleArticleItem(), response=response)`
2. `item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)`
