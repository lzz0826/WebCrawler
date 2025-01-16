# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 要抓取的物件


class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 标题
    title = scrapy.Field()

    # 图片
    img = scrapy.Field()

    # 内容
    content = scrapy.Field()

    # 楼主名
    userName = scrapy.Field()

