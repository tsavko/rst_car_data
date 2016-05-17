import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from rst_car_data.items import RstCarDataItem
from scrapy.http import Request


class RSTSpider(CrawlSpider):
    name = 'rst2'
    allowed_domains = ['rst.ua']
    start_urls = ['http://rst.ua/oldcars/ukraine/1.html']

    rules = [
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(
            allow=['/oldcars/ukraine/[0-9]*.html$', '/oldcars/[A-z]+/.+/.+.html$']),
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
        car_link_structure = re.compile('http://rst.ua/oldcars/[A-z]+/.+/.+.html$')
        for lnk in car_link_full:
            if car_link_structure.match(lnk):
                item = RstCarDataItem()
                item['URL'] = lnk
                request = Request(lnk, callback=self.parse_page)
                request.meta['item'] = item
                yield request


    def parse_page(self, response):
        # car = response.xpath('//h2[contains(@id, "rst-page-oldcars-item-header")]/text()').extract()
        # for c in car:
        #     item = response.meta['item']
        #     item['name'] = c
        #     print item
        #     yield item

        def clean_digits(raw):
            clean = int(''.join([dig for dig in raw if dig.isdigit()]))
            return clean   # extracts numbers from a string

        
        def fuel_translate(orig):
            if orig == u'(\u0411\u0435\u043d\u0437\u0438\u043d)':
                return 'Petrol'

            elif orig == u'(\u0413\u0430\u0437/\u0411\u0435\u043d\u0437\u0438\u043d)':
                return 'LPG/Petrol'

            elif orig == u'(\u0414\u0438\u0437\u0435\u043b\u044c)':
                return 'Diesel'


        def gearbox_translate(orig):
            if orig in [u'\u041c\u0435\u0445\u0430\u043d\u0438\u0447\u0435\u0441\u043a\u0430\u044f',
                		u'\u041c\u0435\u0445\u0430\u043d\u0438\u043a\u0430-4',
                		u'\u041c\u0435\u0445\u0430\u043d\u0438\u043a\u0430-5',
                		u'\u041c\u0435\u0445\u0430\u043d\u0438\u043a\u0430-6']:
                return 'Manual'

            else:
                return 'Automatic'


        def drive_translate(orig):
            if orig == u'(\u041f\u0435\u0440\u0435\u0434\u043d\u0438\u0439 \u043f\u0440\u0438\u0432\u043e\u0434)':
                return 'FWD'

            elif orig == u'(\u0417\u0430\u0434\u043d\u0438\u0439 \u043f\u0440\u0438\u0432\u043e\u0434)':
                return 'RWD'

            else:
                return '4WD'


        def type_check(inp):
            if type(inp) == list:
                out = inp[0]
                return out
            else:
                return inp


        all_data = response.xpath('//div[contains(@id, "rst-page-left-column")]')
        for a in all_data:
            item = response.meta['item']

            item['name'] = type_check(a.xpath('//div[contains(@id, "rst-page-oldcars-tree-block")]/a[4]/text()').extract())

            item['year'] = int(a.xpath('//a[contains(@class, "rst-uix-black rst-uix-bold")]/text()').extract())
            
            item['price_USD'] = clean_digits(a.xpath('//span[contains(@class, "rst-uix-grey")]/text()').extract())

            item['price_UAH'] = clean_digits(a.xpath('//span[contains(@class, "rst-uix-price-param")]/strong/text()').extract())

            item['kilometrage'] = clean_digits(a.xpath('//span[contains(@class, "rst-uix-grey")][2]/text()').extract())

            item['engine_size'] = float(a.xpath('//ul/li[3]/span[2]/strong/text()').extract())

            item['fuel_type'] = fuel_translate(a.xpath('//ul/li[3]/span[2]/span/text()').extract())

            item['gearbox'] = gearbox_translate(a.xpath('//ul/li[4]/span[2]/strong/text()').extract())

            item['drive'] = drive_translate(a.xpath('//ul/li[4]/span[2]/span/text()').extract())

            # print item
            yield item

            # eng = a.xpath('//ul/li[3]/span[2]/strong/text()').extract()

            # eng2 = a.xpath('//table[contains(@class, "rst-uix-table-superline")]/tbody/tr[3]/td[2]/strong/text()').extract()

            # print eng, eng2
            # print len(eng), len(eng2)


# //*[@id="rst-page-oldcars-item"]/div[3]/table/tbody/tr[3]/td[2]/strong
# //*[@id="rst-page-oldcars-item"]/div[3]/ul/li[3]/span[2]/strong
