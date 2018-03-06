# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import random

from .base import BaseTask
from octopus.celery import app

from octopus.collect.models import KongfzInstance

class KongfzSearch(BaseTask):
    abstract = False
    name = 'octopus.tasks.kongfz_search'

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'kongfz']


app.register_task(KongfzSearch())

class KongfzAuctionDetail(BaseTask):
    abstract = False
    name = 'octopus.tasks.kongfz_auction_detail'

    def __init__(self, auction_id):
        self.auction_id = auction_id

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'kongfz_auction_detail', '-a',
                'auction_id=%s' % self.auction_id]

@app.task(bind = True, name = 'octopus.tasks.kongfz_auction_watcher')
def kongfz_auction_watcher(self):
    for instance in KongfzInstance.objects.filter(is_auction = True):
        task = KongfzAuctionDetail(instance.source_id)
        task.apply_async(count_down = random.randint(0, 300))

@app.task(bind = True, name = 'kongfz_sell_watcher')
def kongfz_sell_watcher(self):
    for instance in KongfzInstance.objects.filter(is_auction = False):
        pass