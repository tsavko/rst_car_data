# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class RstCarDataItem(Item):
    # define the fields for your item here like:
    URL = Field()
    name = Field()
    make = Field()
    model = Field()
    year = Field()
    price_USD = Field()
    price_UAH = Field()
    kilometrage = Field()
    engine_size = Field()
    fuel_type = Field()
    gearbox = Field()
    region = Field()
    city = Field()
    drive = Field()
    body_type = Field()
    colour = Field()