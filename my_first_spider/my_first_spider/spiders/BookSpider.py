# 1) Создать пауков по сбору данных о книгах с сайтов labirint.ru и/или book24.ru
# 2) Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги
# 3) Собранная информация должна складываться в базу данных



import scrapy


from scrapy.http import HtmlResponse

from my_first_spider.my_first_spider.items import BooksSpiderItem

class BookSpider(scrapy.Spider):

    name='books'
    start_urls = [ 'https://www.labirint.ru/books/']

    custom_settings = {
        'ITEM_PIPELINES': {
    'my_first_spider.my_first_spider.pipelines.BooksSpiderPipeline': 300,
    },

    'DOWNLOADER_MIDDLEWARES': {
       'my_first_spider.my_first_spider.middlewares.MyFirstSpiderMiddleware': 543,
    }

    }


    def parse(self,response:HtmlResponse):
        urls_books=response.xpath("//div[@class='product-cover__cover-wrapper']/a/@href").getall()
        for url_book in urls_books:
            yield response.follow(url_book,callback=self.parse_book)


    def parse_book(self,response:HtmlResponse):
        name_book_author=response.xpath("//div[@class='prodtitle']/h1/text()").get()
        if name_book_author is None or len(name_book_author.split(":")) < 2:
            return
        url_book=response.url
        name_book=name_book_author.split(":")[1]
        author_book=name_book_author.split(":")[0]
        price_book=response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        price_book_disc=response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating=response.xpath("//div[@id='rate']/text()").get()

        yield BooksSpiderItem(
            url=url_book,
            name=name_book,
            author=author_book,
            price=price_book,
            price_disc=price_book_disc,
            rating=rating
        )
