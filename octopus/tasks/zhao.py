# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from .base import BaseTask
from octopus.celery import app

class ZhaoSearch(BaseTask):
    abstract = False
    name = 'octopus.tasks.zhao_search'

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'zhao']


app.register_task(ZhaoSearch())
