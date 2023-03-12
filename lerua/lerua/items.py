# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst

def clean_price(value):
    try:
        value = int(value[0].strip())
    except ValueError:
        value = float(value[0].strip())
    return value

def clean_name(value):
    return value[0]

def clean_url(value):
    return value[0]

def clean_img(value):
    return set(value)


class LeruaItem(scrapy.Item):
    # define the fields for your item here like:
    url=scrapy.Field(input_processor=Compose(clean_url), output_processor=TakeFirst())  
    name=scrapy.Field(input_processor=Compose(clean_name), output_processor=TakeFirst())  
    price=scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    images=scrapy.Field(input_processor=Compose(clean_img))
    _id = scrapy.Field()
    
