# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pg8000
import json
import logging
import os
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PostgresPipeline(object):
    # Init 
    user            =   os.environ.get('DB_USER' ,'')
    password        =   os.environ.get('DB_PASSWORD', '')
    host            =   os.environ.get('DB_HOSTNAME', '')
    database        =   os.environ.get('DB_DATABASE', '')
    port            =   os.environ.get('DB_PORT', '')
    schema          =   os.environ.get('DB_SCHEMA', '')
    insert_table    =   os.environ.get('DB_INSERT_TABLE', '')
    
    def open_spider(self, spider):
        self.client = pg8000.connect(
                            user=self.user,
                            password = self.password,
                            host = self.host,
                            database = self.database,
                            port = self.port)
        self.curr = self.client.cursor()

    def close_spider(self, spider):
       self.client.close()

    def process_item(self, item, spider):
        # Create table to insert
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS {schema}.{insert_table} (
                RowID uniqueidentifier,
                crawl_date timestamp,
                crawl_ts integer,
                nama_pusat text,
                nama_varieti text,
                harga_tinggi decimal,
                harga_purata decimal,
                harga_rendah decimal,
                PRIMARY KEY (RowID)
            )
        """.format(schema=self.schema, insert_table=self.insert_table)
        )

        self.curr.execute("""
                        INSERT INTO {schema}.{insert_table} VALUES (
                                                                    '{crawlDate}', 
                                                                    '{crawlTimeStamp}',
                                                                    '{NamaPusat}', 
                                                                    '{NamaVarieti}', 
                                                                    '{HargaTinggi}', 
                                                                    '{HargaPurata}', 
                                                                    '{HargaRendah}'
                                                                )
                        ON CONFLICT (gold_code, last_update_ts)
                        DO UPDATE
                        SET 
                            crawl_date = excluded.crawl_date,
                            crawl_ts = excluded.crawl_ts,
                            nama_pusat = excluded.nama_pusat,
                            harga_tinggi = excluded.harga_tinggi,
                            harga_purata = excluded.harga_purata,
                            harga_rendah = excluded.harga_rendah
                        """.format(schema=self.schema, insert_table=self.insert_table, **item)
        )
        self.client.commit()
        logging.info("Upserted a record to the table '{schema}.{insert_table}'".format(schema=self.schema, insert_table=self.insert_table))
        return item