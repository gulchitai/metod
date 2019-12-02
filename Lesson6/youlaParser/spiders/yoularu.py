# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from youlaParser.items import YoulaparserItem
from scrapy.loader import ItemLoader

class YoularuSpider(scrapy.Spider):
    name = 'yoularu'
    allowed_domains = ['youla.ru']
    start_urls = ['https://auto.youla.ru/khabarovsk/cars/used/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[@class="Paginator_block__2XAPy app_roundedBlockWithShadow__1rh6w"]/a[last()]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        ads_links = response.xpath('//article[@class="SerpSnippet_snippet__3O1t2 app_roundedBlockWithShadow__1rh6w"]/div/div/a/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=YoulaparserItem(), response=response)
        loader.add_xpath('title', '//div[@class="AdvertCard_advertTitle__1S1Ak"]/text()')
        loader.add_xpath('photos', '//figure/picture/source/@srcset')
        loader.add_xpath('price', '//div[@data-target="advert-price"]/text()')

        # title = response.xpath('//div[@class="AdvertCard_advertTitle__1S1Ak"]/text()').extract_first()
        # photos = response.xpath('//figure/picture/source/@srcset').extract()
        # print(title, photos)
        # yield YoulaparserItem(title=title, photos=photos)
        yield loader.load_item()
