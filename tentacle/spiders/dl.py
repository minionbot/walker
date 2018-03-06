# -*- coding: utf-8 -*-
import scrapy
import re

from tentacle.items import StampGroupCatalogItem, StampSingleCatalogItem, StampGroupCatalog, StampSingleCatalog

class DlSpider(scrapy.Spider):
    name = 'dl'
    allowed_domains = ['www.chinesestamp.cn']

    total_page = 1

    def start_requests(self):
        return [scrapy.FormRequest(
            'http://www.dlsepu.com/forum.php?mod=forumdisplay&fid=22',
            method = 'GET',
            formdata = {
                'page': '1'
            },
            meta = {
                'page': 1,
            }
        )]

    def parse(self, response):
        page_bar = response.css('#fd_page_top .pg label span::text')
        total_page_text = page_bar.extract()[0]

        match = re.search(r'\D*(\d+).*', total_page_text)
        if not match:
            return {}

        self.total_page = int(match.group(1))

        self.parse_items(response)

    def parse_items(self, response):
        pass