# -*- coding: utf-8 -*-
import scrapy


class XabusinessSpider(scrapy.Spider):
    name = 'xabusiness'
    allowed_domains = ['www.xabusiness.com']
    start_urls = ['http://www.xabusiness.com/']

    def parse(self, response):
        pass
