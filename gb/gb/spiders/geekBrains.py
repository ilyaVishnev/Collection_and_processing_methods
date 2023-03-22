import scrapy

from scrapy.http import FormRequest
from gb.items import GbItem
 
all_possible_choises={}


class GeekbrainsSpider(scrapy.Spider):
    name = "geekBrains"
    allowed_domains = ["gb.ru"]
    start_urls = ["https://gb.ru/login"]
    

    def parse(self, response):
        token=response.xpath("//input[@type='hidden'][@name='authenticity_token']//@value").get() 
        yield FormRequest.from_response(
            response=response,
            method='POST',
            formdata={
            'authenticity_token':token,
            'user[email]':'*****@mail.ru',
            'user[password]':'*******'
            },
            callback=self.parse_page
        )
    
    def parse_page(self,response):
        courses=response.xpath("//a[@class='direction-card']")
        for course in courses:
            yield response.follow(response.url + course.xpath(".//@href").get(),callback=self.parse_courses,meta={"name_course":course.xpath(".//div[@class='direction-card__text']/h5/text()").get()})

        
    def parse_courses(self,response):
        global all_possible_choises
        name_course=response.meta.get('name_course')
        
        spec_list=list()
        specializations=response.xpath("//div[@class='direction-card ui-col-md-6 ui-col-xxxl-6']")
        for spec in specializations:
            spec_list.append(spec.xpath(".//span[@class='direction-card__title-text ui-text-body--1 ui-text--bold']/text()").get())
        yield GbItem (
             courses=spec_list,
             name=name_course
        )
           




 

