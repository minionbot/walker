# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import logging
import re

import scrapy
from django.utils.timezone import datetime
from scrapy_splash import SplashFormRequest as BasicSplashFormRequest
from scrapy_splash import SplashRequest

from octopus.collect.models import QQBBInstance, SELL_AUCTION, SELL_SELLING
from tentacle.items import QQBBInstanceItem
from tentacle.spiders.base import BaseSpider

logger = logging.getLogger('scrapy')

KEYS = [
    '原地 寄',
    '原地封',
    't3', '户县',
    't4', '大庆',
    't5', '大寨',
    't11', '韶山',
    't74', '辽塑',
    't82', '西厢',
    't84', '黄帝陵',
    't89', '簪花仕女图',
    't89m',
    't96', '拙政园',
    't99', '牡丹亭',
    't99m',
    't100', '峨眉山',
    't103', '梅花', '梅园',
    't103m',
    't104', '花灯',
    't108', '航天',
    't110', '白鹤',
    't110m',
    't116', '壁画', '敦煌',
    't121', '名楼',
    't129', '兰花',
    't130', '泰山',
    't131', '三国',
    't132', '麋鹿',
    't137', '儿童生活',
    't138', '水浒',
    't140', '华山',
    't141', '美术作品',
    't143', '火箭',
    't144', '西湖',
    't150',
    't151', '铜马车',
    't155', '衡山',
    't156', '都江堰',
    't158', '夜宴图',
    't162', '杜鹃',
    't163', '衡山',
    't164', '避暑山庄', '承德'
    't166', '瓷器', '景德镇',
    't167',
    '首日 寄',
]

TYPES = [
    #
]

# SEARCHES = itertools.product(KEYS, TYPES)
SEARCHES = KEYS

class SplashFormRequest(BasicSplashFormRequest):

    def __init__(self, url=None, callback=None, method=None, formdata=None,
                 body=None, **kwargs):
        # First init FormRequest to get url, body and method
        if formdata:
            scrapy.FormRequest.__init__(
                self, url=url, method=method, formdata=formdata, **kwargs)
            url, method, body = self.url, self.method, self.body
        # Then pass all other kwargs to SplashRequest
        SplashRequest.__init__(
            self, url=url, callback=callback, method=method, body=body,
            **kwargs)

class QiQiBaBaSpider(BaseSpider):
    name = 'qqbb'
    page_limit = {}
    root = 'https://m.997788.com'
    model = QQBBInstance

    def __init__(self, mode = 'update', **kwargs):
        self.mode = mode
        super(QiQiBaBaSpider).__init__(**kwargs)

    def start_requests(self):

        requests = []
        for search in SEARCHES:
            # search = ' '.join(word)
            requests.extend([
                self.get_request(search.strip(), 1),
            ])

        return requests

    def get_request(self, key, page):
        return SplashFormRequest(
            "https://m.997788.com/all_3/3/164/?d=164&r=&v1=62997&v2=&v3=&v4=&v5=&v6=63008&v7=&v8=&v9=&v10=&v11=&v12=&"
            "t2=0&t4=0&t5=2&t6=&t7=0&t8=0&t9=0&t10=&z=0&p=0&v=0&u=1&y=2&o=o",
            formdata = {
                's0': key
            },
            meta = {
                'page': int(page),
                'search': key
            },
            encoding = 'GB2312',
            method = 'GET',
            cookies = {'h5_localstorage': 'null'}
        )

    def parse(self, response):
        search = response.meta['search']
        page = response.meta['page']

        if self.page_limit.get(search, None) is None:
            total_page_text = response.css('.showpage table tbody tr')[0].css('td')[1].css('font')[1].css('strong '
                                                                                               'font::text').extract_first()
            match = re.search(r'\D*(\d+).*', total_page_text)
            if not match:
                yield {}

            total_page = int(match.group(1))

            # max depth 25
            self.page_limit.setdefault(search, min(total_page, 50))

        imported = True

        items = response.css('#body #both table.tbc.tbc_old')
        for date in items:

            detail_fields = date.css('tbody tr td')[1]
            title_fields = detail_fields.css('p>a::attr(title)').extract_first().rsplit('-', 1)
            if len(title_fields) != 2:
                logger.error('can not parse title from qqbb', extra = {
                    'stack': True,
                })

            is_auction = False
            if title_fields[1].startswith('au'):
                is_auction = True

            source_id = int(title_fields[1][2:])
            if source_id in self.imported_instances():
                continue

            title = title_fields[0]

            image_url = date.css('tbody tr td')[0].css('a img::attr(src)').extract_first()
            reference = date.css('tbody tr td')[0].css('a::attr(href)').extract_first()
            reference = self.root + reference

            click = date.css('div.art_1>div.art_2>a')[-1].css('a::attr(onclick)').extract_first()
            click = click.replace('this.href=', '')

            click = click.strip("'").strip('/')
            shop_id = click.split('/')[0]

            price = date.css('div.art_1>div.art_3>.font_price::text').extract_first()
            price = price.strip('￥')
            price = price.replace(',', '')

            imported = False

            item = QQBBInstanceItem()
            item['name'] = title
            item['is_auction'] = is_auction
            item['source_id'] = source_id
            item['image_url'] = image_url
            item['reference'] = reference
            item['price'] = price
            item['shop_id'] = shop_id
            item['stage'] = SELL_AUCTION if is_auction else SELL_SELLING
            item['search_key'] = search
            item['put_on_date'] = datetime.now()
            item.save()

            self.ids.add(int(item['source_id']))

        if page < self.page_limit[search] and not imported:
            yield self.get_request(search, page + 1)

        yield {}
