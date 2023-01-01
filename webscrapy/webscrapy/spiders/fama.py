import scrapy
from datetime import datetime
import time
import json
from ..items import WebscrapyDailyCommodityItem

class FamaSpider(scrapy.Spider):
    name = 'fama'
    allowed_domains = ['https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt=2022/12/29&PricingDtPrev=2022/12/27']
    start_urls = ['https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt=2022/12/29&PricingDtPrev=2022/12/27']


    def parse(self, response):

        pusat = response.xpath("/html/body/table/tr/td")

        for p in pusat:

            # Create an object of Item class
            item = WebscrapyDailyCommodityItem()

            item["NamaPusat"] = p.xpath(".//table[position() mod 2 = 1]/tr/td/b/text()").extract()
            item["NamaVarieti"] = p.xpath(".//table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[1]/text()").extract()
            item["UnitBarang"] = p.xpath(".//table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[3]/text()").extract()
            item["HargaTinggi"] = p.xpath(".//table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[4]/text()").extract()
            item["HargaPurata"] = p.xpath(".//table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[5]/text()").extract()
            item["HargaRendah"] = p.xpath(".//table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[6]/text()").extract()


            #//*[@id="D101"]/td[1] /html/body/table/tbody/tr[5]/td/table[2]/tbody/tr[3]/td[1]
            #/html/body/table/tbody/tr[5]/td/table[1]/tbody/tr/td/b