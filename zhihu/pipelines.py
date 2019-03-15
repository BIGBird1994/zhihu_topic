# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.parse
from pymongo import MongoClient


class ZhihuPipeline(object):
    def __init__(self,conn):
        super().__init__()
        self.col = conn['zhihu']['fashion_answer']


    def process_item(self, item, spider):
        try:
            self.col.insert(dict(item))
            return item
        except Exception as e:
            print(e)
