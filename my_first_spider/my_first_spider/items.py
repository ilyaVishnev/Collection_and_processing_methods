
import scrapy



class BooksSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    name=scrapy.Field()
    author=scrapy.Field()
    price=scrapy.Field()
    price_disc=scrapy.Field()
    rating=scrapy.Field()
    _id = scrapy.Field()
