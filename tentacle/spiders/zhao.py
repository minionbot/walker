# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals
import scrapy
import json

from octopus.collect.models import ZhaoInstance, SELL_AUCTION, SELL_ENDED, SELL_PREVIEW
from tentacle.items import ZhaoInstanceItem
from tentacle.conf import SEARCHES

from cached_property import cached_property


class ZhaoSpider(scrapy.Spider):
    name = 'zhao'

    def __init__(self, mode = 'update', **kwargs):
        self.mode = mode
        super(ZhaoSpider).__init__(**kwargs)

    def start_requests(self):
        requests = []
        for word in SEARCHES:
            requests.extend([
                self.get_auction_request(word, 1),
                self.get_preview_request(word, 1)
            ])

        return requests

    @cached_property
    def imported_instances(self):
        return ZhaoInstance.objects.values_list('source_id', flat = True).order_by('-source_id')

    def get_auction_request(self, key, page):
        return self._get_request(key = key, page = page, stage = '2')

    def get_preview_request(self, key, page):
        return self._get_request(key = key, page = page, stage = '1')

    def _get_request(self, key, page, stage):
        return scrapy.FormRequest(
            "https://search.zhaoonline.com/search",
            formdata = {
                'stage': str(stage),  # preview
                'q': str(key),
                'category': '467',  # 新中国
                'page': str(page),
                'perPage': '100',
                'from': 'zhaoonline'
            },
            meta = {
                'stage': str(stage),
                'page': int(page),
                'search': str(key)
            },
            method = 'GET',
        )

    def parse(self, response):
        body = json.loads(response.body_as_unicode())
        page = response.meta['page']

        stage = response.meta['stage']
        search = response.meta['search']
        action_type = SELL_PREVIEW if stage == '1' else SELL_AUCTION

        if len(body['list']) == 0:
            yield body

        all_imported = True

        for it in body['list']:
            if it['auctionNo'] in self.imported_instances:
                continue

            # save item
            item = ZhaoInstanceItem()
            item['name'] = it['title']
            item['source_id'] = it['auctionNo']
            item['image_url'] = it['images'][0]['url']
            item['price'] = float(it['price'] + it['serviceFee'])
            item['reference'] = 'http://www.zhaoonline.com/xinzhongguofengpianjian/{}.shtml'.format(it['auctionNo'])
            item['put_on_date'] = it['startAt']
            item['begin_time'] = it['startAt']
            item['stage'] = action_type
            item['search_key'] = search

            instance = item.save()
            all_imported = False

        if self.mode == 'init' or not all_imported:
            yield self._get_request(search, page + 1, stage)

        yield body
