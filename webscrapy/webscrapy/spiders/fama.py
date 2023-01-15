import scrapy
from datetime import datetime
from ..items import WebscrapyDailyCommodityItem
from scrapy.http import Request
import pandas as pd


class FamaSpider(scrapy.Spider):
    name = 'fama'
    start_urls = ['https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt=2015/01/01&PricingDtPrev=2015/01/01']


    def parse(self, response):

        start_date = '2015/01/01'
        end_date = '2023/01/09'
        dateRange = pd.date_range(start_date,end_date)
        urls = ['https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt={0}&PricingDtPrev={0}'.format(i) for i in dateRange.strftime('%Y/%m/%d')]
        for url in urls: 
            Request(url, callback=self.parse_page)

    def parse_page(self, response):
        

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
            item["Timestamp"] = datetime.date()
            print(p.xpath(".//table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[4]/text()").extract())

            