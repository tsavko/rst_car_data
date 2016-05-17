# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from rst_car_data.items import RstCarDataItem


class ParserSpider(CrawlSpider):
    name = 'parser'
    allowed_domains = ['rst.ua']
    start_urls = ['http://rst.ua/oldcars/ukraine/']

    rules = [
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(
            allow=['http://rst.ua/oldcars/[A-z]+/\w+/\w+.html$']),
            callback='extract_car_data',
            follow=True
            )

        # # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    ]

    def extract_car_data(self, response):
        # car_link = response.css('a.rst-ocb-i-a')
        sel = response.xpath('//ul[contains(@class, "rst-uix-list-superline")]').extract()
        print sel
        # car_link_full = ['http://rst.ua' + i for i in car_link]
        # for lnk in car_link_full:
        #     item = RstCarDataItem()
        #     item['link'] = lnk
        #     yield item