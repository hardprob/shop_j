# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class JdscItem(Item):
    title = Field()
    url = Field()
    price = Field()
    youhui = Field()

