# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(values):
    return values[:values.find(',')-3]

def cleaner_price(values):
    return int(''.join([i for i in values if i.isdigit()]))

class YoulaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(cleaner_price))
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    # title = scrapy.Field()
    # photos = scrapy.Field()


