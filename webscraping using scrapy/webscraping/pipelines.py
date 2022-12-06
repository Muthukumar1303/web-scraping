# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class WebscrapingPipeline:
    def __init__(self) -> None:
        self.create_connection()
        self.create_table()
        
    def create_connection(self):
        self.conn= sqlite3.connect("amazon.db")
        self.cur = self.conn.cursor()
        
    def create_table(self):
        self.cur.execute("""
            create table if not exists amazon (
                image_path text,
                product_name text,
                product_price text,
                ratings text   
            )
            """)
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self,item):
        self.cur.execute("insert into amazon values(?,?,?,?)",
                         (item['image_path'],item['product_name'],item['product_price'],item['ratings']))
        self.conn.commit()
