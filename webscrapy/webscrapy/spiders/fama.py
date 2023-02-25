import scrapy
from datetime import datetime
from ..items import WebscrapyDailyCommodityItem
from scrapy.http import Request
import pandas as pd
import numpy as np

class FamaSpider(scrapy.Spider):
    name = 'fama'
    start_urls = ['https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt=2015/01/01&PricingDtPrev=2015/01/01']


    def parse(self, response):

        start_date = '2015/01/01'
        end_date = '2023/01/09'
        dateRange = pd.date_range(start_date,end_date)
        urls = ['https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt={0}&PricingDtPrev={0}'.format('2015/01/01')]
        for url in urls: 
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        

        barang = response.xpath("/html/body/table/tr/td/table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[1]/text()")
        namapusat = response.xpath("/html/body/table/tr/td/table[position () mod 2 = 1]/tr/td/b/text()").extract()


        
        x = 1
        for table in response.xpath("/html/body/table/tr/td/table"):

            if x % 2 == 1:

                pusat = table.xpath(".//tr/td/b/text()").extract()
            
            x = x+1

             

            for p in table.xpath(".//tr[contains(@id,content-body)][position() > 2]"):

                # Create an object of Item class
                item = WebscrapyDailyCommodityItem()
                today = datetime.now()


                item["NamaPusat"]  = pusat
                item["NamaVarieti"] = p.xpath(".//td[1]/text()").extract()
                item["UnitBarang"] = p.xpath(".//td[3]/text()").extract()
                item["HargaTinggi"] = p.xpath(".//td[4]/text()").extract()
                item["HargaPurata"] = p.xpath(".//td[5]/text()").extract()
                item["HargaRendah"] = p.xpath(".//td[6]/text()").extract()
                item["dateTime"] = today

                yield item
                