# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import random

from .base import BaseTask
from octopus.collect.models import ZhaoInstance, SELL_ENDED
from octopus.celery import app

class ZhaoSearch(BaseTask):
    abstract = False
    name = 'octopus.tasks.zhao_search'

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'zhao']


app.register_task(ZhaoSearch())

class ZhaoAuctionDetail(BaseTask):
    abstract = False
    name = 'octopus.tasks.zhao_auction_detail'

    def build_args(self, **kwargs):
        item_id = kwargs['item_id']
        return ['scrapy', 'crawl', 'zhao_auction', '-a',
                'source_id=%s' % item_id]


app.register_task(ZhaoAuctionDetail())

@app.task(bind = True, name = 'octopus.tasks.zhao_auction_watcher')
def zhao_auction_watcher(self):
    for instance in ZhaoInstance.objects.filter(is_auction = True).exclude(stage = SELL_ENDED):
        task = ZhaoAuctionDetail()
        task.apply_async(kwargs = {
            'item_id': instance.item_id
        }, count_down = random.randint(0, 300))
