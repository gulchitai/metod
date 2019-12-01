# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']


    def parse(self, response: HtmlResponse):
        main_link = 'https://www.superjob.ru'
        next_page = response.xpath('//a[@class=\'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe\']/@href').extract_first()
        yield response.follow(main_link + next_page, callback=self.parse)

        vacansy_items = response.xpath('//div[@class=\'_2g1F-\']/a/@href').extract()
        for link in vacansy_items:
            yield response.follow(main_link + link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1[@class=\'_3mfro rFbjy s1nFK _2JVkc\']/text()').extract_first()
        link_v = response.url
        salary = response.xpath('//span[@class=\'_3mfro _2Wp8I ZON4b PlM3e _2JVkc\']/span/text()').extract()
        print(name, link_v, salary)
        yield JobparserItem(name=name, salary=salary, link_v=link_v)
