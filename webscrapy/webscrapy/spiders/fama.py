import scrapy
import datetime
import time
import json

class FamaSpider(scrapy.Spider):
    name = 'fama'
    allowed_domains = ['sdvi2.fama.gov.my']
    start_urls = ['http://sdvi2.fama.gov.my/']

    today = datetime.now().strftime("%Y/%m/%d")

    log_file = f'GetGold/logs/{today}.log'
    custom_settings = {'LOG_LEVEL': 'INFO', 'LOG_FILE': log_file}

    def start_requests(self):
        utc_time = datetime.utcnow()
        crawl_ts = int(time.time())
        crawl_dt = str(crawl_ts)
        yield scrapy.Request(
                url=self.url,  
                headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
                },
                callback=self.parse,
                meta = {
                    'crawl_ts': crawl_ts,
                    'crawl_dt' : crawl_dt,
                    'utc_time': utc_time  
                }
        )

    def parse(self, response):
        
        utc_time = response.meta['utc_time']
        crawl_ts = response.meta['crawl_ts']
        crawl_dt = response.meta['crawl_dt']
        json_response = json.loads(response.text)
        data = json_response.get('data')
        for record in data:
            yield {
                'buyingPrice': record['buyingPrice'],
                'sellingPrice': record['sellingPrice'],
                'goldCode': record['code'],
                'sellChange': record['sellChange'],
                'sellChangePercent': record['sellChangePercent'],
                'buyChange': record['buyChange'],
                'buyChangePercent': record['buyChangePercent'],
                'lastUpdate': str(int(datetime.datetime.strptime(record['dateTime']))),
                'lastUpdateTimeStamp': int(datetime.datetime.strptime(record['dateTime'])),
                'crawlDate': crawl_dt,
                'crawlTimeStamp': crawl_ts
            }