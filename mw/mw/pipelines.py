# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from functools import reduce
import os


import pymongo
class MwPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        dict_item = dict(item)
        self.insert_unique(dict_item, spider)
        return item

    def insert_unique(self, item, spider):

        if hasattr(spider, "duplicity_condition") and spider.duplicity_condition:
            self.__replace_item(item, spider)
        else:
            raise Exception("UndefinedAttribute: duplicity_condition should be specified.")

    def __replace_item(self, item, spider):
        search_dict = {}
        for field in spider.duplicity_condition:
            dict_field = self.__get_dict_field_by_dot_notation(item, field)
            if dict_field:
                search_dict[field] = dict_field
        if search_dict:
            self.db[spider.mongo_collection].replace_one(search_dict, item, upsert=True)
        else:
            self.db[spider.mongo_collection].insert_one(item)

    def __get_dict_field_by_dot_notation(self, item, field):
        keys = field.split(".")
        return reduce(lambda d, key: d.get(key) if d else None, keys, item)
