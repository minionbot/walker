# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import random

from .base import BaseTask
from octopus.celery import app
from octopus.collect.models import KongfzInstance, SELL_ENDED

class KongfzSearch(BaseTask):
    abstract = False
    name = 'octopus.tasks.kongfz_search'

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'kongfz']


app.register_task(KongfzSearch())

class KongfzAuctionDetail(BaseTask):
    abstract = False
    name = 'octopus.tasks.kongfz_auction_detail'

    def build_args(self, **kwargs):
        auction_id = kwargs['auction_id']
        return ['scrapy', 'crawl', 'kongfz_auction', '-a',
                'auction_id=%s' % auction_id]


app.register_task(KongfzAuctionDetail())


class KongfzRetailDetail(BaseTask):
    abstract = False
    name = 'octopus.tasks.kongfz_retail_detail'

    def build_args(self, **kwargs):
        source_id = kwargs['source_id']
        shop_id = kwargs['shop_id']
        return ['scrapy', 'crawl', 'kongfz_retail', '-a',
                'source_id=%s' % source_id, '-a', 'shop_id=%s' % shop_id]


app.register_task(KongfzRetailDetail())

@app.task(bind = True, name = 'octopus.tasks.kongfz_auction_watcher')
def kongfz_auction_watcher(self):
    for instance in KongfzInstance.objects.filter(is_auction = True).exclude(stage = SELL_ENDED):
        task = KongfzAuctionDetail()
        task.apply_async(kwargs = {
            'auction_id': instance.source_id
        }, count_down = random.randint(0, 300))

@app.task(bind = True, name = 'octopus.tasks.kongfz_retail_watcher')
def kongfz_retail_watcher(self):
    for instance in KongfzInstance.objects.filter(is_auction = False).exclude(stage = SELL_ENDED):
        task = KongfzRetailDetail()
        task.apply_async(kwargs = {
            'shop_id': instance.shop_id,
            'source_id': instance.source_id
        }, count_down = random.randint(0, 300))


