# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy252

    def process_item(self, item, spider):
        item['salary_min'], item['salary_max'] = self.salaryHH(item['salary'])
        if spider.name == 'hhru':
            item['site'] = 'https://hh.ru/'
        elif spider.name == 'sjru':
            item['site'] = 'https://superjob.ru/'
        print(item)
        collection = self.mongo_base[spider.name]

        collection.insert_one(item)


        return item

    def salaryHH(self, salaryArray:list):
        salaryStr = ''
        for s in salaryArray:
            salaryStr = salaryStr + s
        nonBreakSpace = u'\xa0'
        salaryStr = salaryStr.replace(nonBreakSpace, '')
        salaryStr = salaryStr.replace(' ', '')
        salary_min = 0
        salary_max = 0
        array = [int(n) for n in ''.join(c if c.isdigit() else ' ' for c in salaryStr).split()]
        if salaryStr[:2] == 'до' and len(array) == 1:
            salary_max = array[0]
        elif salaryStr[:2] == 'от' and len(array) == 1:
            salary_min = array[0]
        elif len(array) == 2:
            salary_min = array[0]
            salary_max = array[1]
        return salary_min, salary_max
