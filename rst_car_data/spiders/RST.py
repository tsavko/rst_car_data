import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from rst_car_data.items import RstCarDataItem

car_links = []
limit_no = 100
i = 0

class RSTSpider(CrawlSpider):
    name = 'rst'
    allowed_domains = ['rst.ua']
    start_urls = ['http://rst.ua/oldcars/ukraine/1.html']

    rules = [
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(
            allow=['/oldcars/ukraine/[0-9]*.html$']),
            callback='extract_car_link',
            follow=True
            )

        # # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    ]

    def extract_car_link(self, response):
        # car_link = response.css('a.rst-ocb-i-a')
        car_link = response.xpath('//a[contains(@class, "rst-ocb-i-a")]/@href').extract()
        car_link_full = ['http://rst.ua' + i for i in car_link]
        for lnk in car_link_full:
            item = RstCarDataItem()
            item['link'] = lnk
            yield item


        # car_links.extend(car_link_full)
        # print car_links
        # return car_links
        # print car_link
        # yield car_link

