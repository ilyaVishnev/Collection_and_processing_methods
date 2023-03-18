# 1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
# ● название;
# ● все фото;
# ● ссылка;
# ● цена.

# Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lerua.items import LeruaItem


class LeruaSpbSpider(scrapy.Spider):

    name = "lerua_spb"
    start_urls = ["https://www.maxidom.ru/catalog/dushevye-kabiny/"]

    def parse(self, response:HtmlResponse):
        next_page=response.xpath("//a[@id='navigation_3_next_page test']/@href").get()
        yield response.follow(response.url,callback=self.parse_page)
        if next_page is None:
            return
        yield response.follow(next_page,callback=self.parse_page)

    def parse_page(self,response:HtmlResponse):
        next_value=response.xpath("//a[@class='img_href']/@href").getall()
        for val in next_value:
            yield response.follow(val,callback=self.parse_instr)


    def parse_instr(self,response:HtmlResponse):

        loader=ItemLoader(item=LeruaItem(),response=response)
        loader.add_value('url',response.url)
        loader.add_xpath('name',"//div[@class='maxi_container']/h1/text()")
        loader.add_xpath('price',"//div[@itemprop='price']/text()")
        loader.add_xpath('images',"//a[@class='product-image']/@href")
        
        yield loader.load_item()



         


