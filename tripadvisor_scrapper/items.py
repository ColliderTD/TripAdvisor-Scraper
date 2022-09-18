# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    name = scrapy.Field()
    site = scrapy.Field()
    phone = scrapy.Field()
    menu = scrapy.Field()
    punctuation = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()

class RestaurantResultItem(scrapy.Item):
    title = scrapy.Field()
    page_link = scrapy.Field()