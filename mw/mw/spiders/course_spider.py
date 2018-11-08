import pdb
from datetime import datetime, timedelta
import scrapy
import pymongo
from scrapy.spiders import CrawlSpider
from scrapy import Request
from scrapy.utils.project import get_project_settings
from urlparse import urlparse
from ..items import CourseItem


class CourseSpider(CrawlSpider):
    name = 'course'
    mongo_collection = 'course'
    duplicity_condition = ['id']

    def __init__(self, delta=""):
        super(CourseSpider, self).__init__()

    def start_requests(self):
        base_url = 'https://matriculaweb.unb.br/graduacao/curso_rel.aspx?cod={}'
        urls_code = ['1', '2', '3', '4']
        for code in urls_code:
            yield scrapy.Request(url=base_url.format(code), callback=self.parse_items)

    def parse_items(self, response):
        for div in response.xpath('//*[@id="datatable"]/tr')[1:]:
            item = CourseItem()
            item['id'] = div.xpath('td[2]/text()').extract()[0]
            item['name'] = div.xpath('td[3]/a/text()').extract()[0]
            yield item
