# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import random

from .base import BaseTask
from octopus.collect.models import QQBBInstance, SELL_ENDED
from octopus.celery import app

class QQBBSearch(BaseTask):
    abstract = False
    name = 'octopus.tasks.qqbb_search'

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'qqbb']


app.register_task(QQBBSearch())

