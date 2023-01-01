# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapyDailyCommodityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #location of [product variety price report
    NamaPusat = scrapy.Field()

    #Name of daily commodity product
    NamaVarieti = scrapy.Field()

    #Unit measurement of product
    UnitBarang = scrapy.Field()

    #Average reported price of one unit of product
    HargaPurata = scrapy.Field()

    #Highest reported price of one unit of product
    HargaTinggi = scrapy.Field()

    #Lowest reported price of one unit of product
    HargaRendah = scrapy.Field()
    
