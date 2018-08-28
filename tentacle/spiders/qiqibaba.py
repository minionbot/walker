# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import logging
import re

from django.utils.timezone import datetime

from octopus.collect.models import QQBBInstance, SELL_AUCTION, SELL_SELLING
from tentacle.items import QQBBInstanceItem
from tentacle.spiders.base import BaseSpider, SplashFormRequest

logger = logging.getLogger('scrapy')

from tentacle.conf import SEARCHES

# no need for append suffix
SEARCHES = SEARCHES

BLACK_SHOP = [
    33068,
    40167
]

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
            pg_tr = response.css('.showpage table tbody tr')[0]
            pg_td = pg_tr.css('td')[1]
            pg_font = pg_td.css('font')[1]
            total_page_text = pg_font.css('strong font::text').extract_first()
            match = re.search(r'\D*(\d+).*', total_page_text)
            if not match:
                yield {}

            total_page = int(match.group(1))

            # max depth 25
            self.page_limit.setdefault(search, min(total_page, 50))

        imported = True

        items = response.css('#body #both table.tbc.tbc_old')
        for date in items:
            title_text = date.css('tbody tr td')[0].css('a img::attr(alt)').extract_first()
            title_fields = title_text.rsplit('(', 1)

            if len(title_fields) != 2:
                logger.error('can not parse title from qqbb', extra = {
                    'stack': True,
                })

            source_fields = str(title_fields[1]).split(')', 1)

            is_auction = False
            if source_fields[0].startswith('au'):
                is_auction = True

            source_id = int(source_fields[0][2:])
            if source_id in self.imported_instances():
                continue

            title = title_fields[0]

            image_url = date.css('tbody tr td')[0].css('a img::attr(src)').extract_first()
            reference = date.css('tbody tr td')[0].css('a::attr(href)').extract_first()
            reference = self.root + reference

            click = date.css('div.art_1>div.art_2>a')[-1].css('a::attr(onclick)').extract_first()
            click = click.replace('this.href=', '')

            click = click.strip("'").strip('/')
            shop_id = int(click.split('/')[0])
            if shop_id in BLACK_SHOP:
                continue

            price = date.css('div.art_1>div.art_3>.font_price::text').extract_first()
            price = price.strip('￥')
            price = float(price.replace(',', ''))

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
