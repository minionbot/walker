# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from .base import BaseTask
from octopus.celery import app

class KongfzSearch(BaseTask):
    abstract = False
    name = 'octopus.tasks.kongfz_search'

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'kongfz']


app.register_task(KongfzSearch())
