# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
import logging
import scrapy
import pymongo
from pymongo.server_api import ServerApi


class MongoDBPipeline(object):

    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings.get('MONGODB_URL'),
            server_api=ServerApi('1')
        )
        db = connection[settings.get('MONGODB_DB')]
        self.collection = db[settings.get('MONGODB_COLLECTION')]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.debug("Question added to MongoDB database!")
        return item