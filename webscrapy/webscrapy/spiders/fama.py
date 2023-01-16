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
        urls = ['https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt={0}&PricingDtPrev={0}'.format('2015/01/01')]
        for url in urls: 
            yield Request(url, callback=self.parse_page)
#for i in dateRange.strftime('%Y/%m/%d')
    def parse_page(self, response):
        

        barang = response.xpath("/html/body/table/tr/td/table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[1]/text()")

        for p in range(len(barang)):

            # Create an object of Item class
            item = WebscrapyDailyCommodityItem()

            index_pusat = p % 36
            print(index_pusat)

            item["NamaPusat"] = response.xpath("/html/body/table/tr/td/table[position () mod 2 = 1]/tr/td/b/text()").extract()[index_pusat]
            #item["NamaPusat"] = response.xpath("/html/body/table/tr/td").extract()
            item["NamaVarieti"] = response.xpath("/html/body/table/tr/td/table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[1]/text()").extract()[p]
            item["UnitBarang"] = response.xpath("/html/body/table/tr/td/table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[3]/text()").extract()[p]
            item["HargaTinggi"] = response.xpath("/html/body/table/tr/td/table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[4]/text()").extract()[p]
            item["HargaPurata"] = response.xpath("/html/body/table/tr/td/table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[5]/text()").extract()[p]
            item["HargaRendah"] = response.xpath("/html/body/table/tr/td/table[position() mod 2 = 0]/tr[contains(@id,content-body)][position() > 2]/td[6]/text()").extract()[p]
            item["dateTime"] = datetime.now()

            yield item
            