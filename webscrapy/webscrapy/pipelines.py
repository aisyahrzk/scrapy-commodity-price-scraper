# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pg8000
import logging
import psycopg2
import config.constant as config
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PostgresPipeline(object):
    # Init 
    user            =   config.DB_USER
    password        =   config.DB_PASSWORD
    host            =   config.DB_HOSTNAME
    database        =   config.DB_DATABASE
    port            =   config.DB_PORT
    insert_table    =   config.DB_INSERT_TABLE
    schema          =   config.DB_SCHEMA
    
    def open_spider(self, spider):
        self.client = psycopg2.connect(
                            user=self.user,
                            password = self.password,
                            host = self.host,
                            database = self.database,
                            port = self.port)
        self.curr = self.client.cursor()

    def close_spider(self, spider):
       self.client.close()


    def process_item(self, item, spider):

        values = (item["dateTime"],str(item["NamaPusat"][0]),str(item["NamaVarieti"][0]) ,item["HargaTinggi"][0] ,item["HargaPurata"][0],item["HargaRendah"][0],item["UnitBarang"][0])
        print(values)
        query =  """INSERT INTO fama.dailycommodity_price (crawl_date,nama_pusat,nama_varieti,harga_tinggi,harga_purata,harga_rendah,unit_barang) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        self.curr.execute(query,values)
        self.client.commit()
        logging.info("Inserted a record to the table '{schema}.{insert_table}'".format(schema=self.schema, insert_table=self.insert_table))
        return item