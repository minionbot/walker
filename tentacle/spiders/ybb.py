# -*- coding: utf-8 -*-
import re
import scrapy

class ChinesestampSpider(scrapy.Spider):
    name = 'ybb'
    allowed_domains = ['www.china-ybb.com']
    start_urls = [
        'http://www.china-ybb.com/list/4k',
    ]

    def parse(self, response):
        # 获取页码
        pages = response.css('body>div#mulu>div.mrfy>a::attr(href)').extract()
        current_page = response.css('body>div#mulu>div.mrfy>a.active::attr(href)').extract()[0]

        index = pages.index(current_page)
        url = response.request.url

        self.logger.info("scraping %s", url)

        self.parse_list_page(response)

        # has more page
        if index + 1 < len(pages):
            fragments = url.split('/')
            fragments[-1] = pages[index + 1]
            yield scrapy.Request('/'.join(fragments), callback = self.parse)

        yield {}

    def parse_list_page(self, response):
        pass