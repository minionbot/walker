# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals
import scrapy
import json

from octopus.collect.models import KongfzInstance, SELL_AUCTION, SELL_SELLING
from tentacle.items import KongfzInstanceItem
from tentacle.conf import SEARCHES

from cached_property import cached_property

from django.utils.timezone import datetime


class KongfzSpider(scrapy.Spider):
    name = 'kongfz'

    def __init__(self, mode = 'update', **kwargs):
        self.mode = mode
        super(KongfzSpider).__init__(**kwargs)

    def start_requests(self):
        requests = []
        for word in SEARCHES:
            requests.extend([
                self.get_sell_request(word, 1),
                self.get_auction_request(word, 1)
            ])

        return requests

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
                'page': int(page),
                'search': str(key)
            }
        )

    def get_auction_request(self, key, page):
        return scrapy.FormRequest(
            "https://app.kongfz.com/auction/searchAuction",
            formdata = {
                'UserAgent': 'IOS_KFZ_COM_2.0.7_iPhone 7 Plus_10.3.3',
                'catId': '36',
                'key': str(key),
                'order': '-1',
                'page': str(page),
                'type': '1',
            },
            meta = {
                'page': int(page),
                'search': str(key)
            }
        )

    def parse(self, response):
        body = json.loads(response.body_as_unicode())
        page = response.meta['page']
        search = response.meta['search']

        if len(body['list']) == 0:
            yield body

        imported = True
        is_auction = 'searchAuction' in response._get_url()

        for it in body['list']:
            if it['id'] in self.imported_instances:
                continue

            # save item
            item = KongfzInstanceItem()
            item['name'] = it['name']
            item['source_id'] = it['id']
            item['image_url'] = it['smallImg']
            item['is_auction'] = is_auction
            item['stage'] = SELL_AUCTION if is_auction else SELL_SELLING
            item['shop_id'] = it['shopId']
            if is_auction:
                item['price'] = float(it['beginPrice'])
                item['reference'] = 'http://m.kongfz.cn/{}'.format(it['id'])
                item['put_on_date'] = datetime.fromtimestamp(it['beginTime'])
                item['begin_time'] = datetime.fromtimestamp(it['beginTime'])
                item['end_time'] = datetime.fromtimestamp(it['endTime'])
            else:
                item['price'] = float(it['price'])
                item['reference'] = 'http://book.kongfz.com/{}/{}/'.format(it['shopId'], it['id'])
                item['put_on_date'] = it['date']
            instance = item.save()
            imported = False

        if self.mode == 'init' or not imported:
            if is_auction:
                yield self.get_auction_request(search, page + 1)
            else:
                yield self.get_sell_request(search, page + 1)

        yield body
