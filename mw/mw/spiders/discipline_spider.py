import pdb
from datetime import datetime, timedelta
import scrapy
import pymongo
from scrapy.spiders import CrawlSpider
from scrapy import Request
from scrapy.utils.project import get_project_settings
from urlparse import urlparse
from ..items import DisciplineItem
from pymongo import MongoClient
import re

class DisciplineSpider(CrawlSpider):
    name = 'discipline'
    mongo_collection = 'discipline'
    duplicity_condition = ['codigo']

    def __init__(self, delta=""):
        super(DisciplineSpider, self).__init__()

    def start_requests(self):
        client = MongoClient('localhost', 27017)
        db = client['mw']
        collection = db['course']
        base_url = 'https://matriculaweb.unb.br/graduacao/curso_dados.aspx?cod={}'

        for obj in collection.find():
            yield scrapy.Request(url=base_url.format(obj.get('id').encode()), callback=self.get_links)

    def get_links(self, response):
        link =  response.xpath('/html/body/section/div/div[3]/div/div/div[2]/div[1]/a[2]/@href').extract()[0].encode()
        cod = re.compile('cod=(.*)').findall(link)[0]
        base_url = 'https://matriculaweb.unb.br/graduacao/curriculo.aspx?cod={}'
        yield scrapy.Request(url=base_url.format(cod), callback=self.parse_items)

    def parse_items(self, response):
        base_url = 'https://matriculaweb.unb.br{}'
        tables = response.xpath('/html/body/section/div/div[3]/div/div/div[2]//table')
        for table in tables[1:]:
            for row in table.xpath('tr'):
                try:
                    link = row.xpath('td[2]/a/@href').extract()[0].encode()
                    yield scrapy.Request(url=base_url.format(link), callback=self.get_disciplines)
                except:
                    pass

    def get_disciplines(self, response):
        import pdb; pdb.set_trace()
        item = DisciplineItem()
        item['nome'] = response.xpath('/html/body/section/div/div[3]/div/div/div/h2/text()').extract()[0].encode('utf-8').strip()
        item['codigo'] = re.compile('cod=(.*)').findall(response.url)[0]
        for row in response.xpath('//*[@id="datatable"]/tr'):
            header_list = '\n'.join(row.xpath('th//text()').extract())
            header = header_list.encode('utf-8')
            content_list = '\n'.join(row.xpath('td//text()').extract())
            content = content_list.encode('utf-8')
            if header in ['Ementa', 'Programa', 'Bibliografia']:
                item[header.lower()] = content

        yield item
