# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    # define the fields for your item here like:
    quotes = scrapy.Field()
    author = scrapy.Field()

class AmazonSaItem(scrapy.Item):
    # define the fields for your item here like:
    image_path = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    ratings = scrapy.Field()