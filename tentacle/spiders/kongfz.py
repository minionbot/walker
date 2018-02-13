# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals
import scrapy
import json

from octopus.collect.models import KongfzInstance
from tentacle.items import KongfzInstanceItem

from cached_property import cached_property

class KongfzSpider(scrapy.Spider):
    name = 'kongfz'

    def __init__(self, mode = 'update', **kwargs):
        self.mode = mode
        super(KongfzSpider).__init__(**kwargs)

    def start_requests(self):
        return [
            self.get_sell_request('原地', 1)
        ]

    @cached_property
    def imported_instances(self):
        return KongfzInstance.objects.values_list('source_id', flat = True).order_by('-source_id')

    def get_sell_request(self, key, page):
        return scrapy.FormRequest(
            "https://app.kongfz.com/shop/newFilterBooks",
            formdata = {
                'UserAgent': 'IOS_KFZ_COM_2.0.7_iPhone 7 Plus_10.3.3',
                'author': '',
                'catId': '36',
                'exKey': '',
                'itemName': '',
                'key': str(key),
                'listBook': '1',
                'maxPrice': '0',
                'minPrice': '0',
                'order': '-4',
                'page': str(page),
                'params': json.dumps([
                    {
                        "cid": "36",
                        "cname": "全部邮票税票"
                    }
                ]),
                'press': '',
                'shopName': ''
            },
            meta = {
                'page': int(page)
            }
        )

    def parse(self, response):
        body = json.loads(response.body_as_unicode())
        page = response.meta['page']

        if len(body['list']) == 0:
            yield body

        imported = True
        for it in body['list']:
            if it['id'] in self.imported_instances:
                continue

            # save item
            item = KongfzInstanceItem()
            item['price'] = float(it['price'])
            item['name'] = it['name']
            item['source_id'] = it['id']
            item['image_url'] = it['smallImg']
            item['reference'] = 'http://book.kongfz.com/{}/{}/'.format(it['shopId'], it['id'])
            item['put_on_date'] = it['date']
            instance = item.save()
            imported = False

        if self.mode == 'init' or not imported:
            yield self.get_sell_request('原地', page + 1)

        yield body
