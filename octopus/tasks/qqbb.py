# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from octopus.celery import app
from .base import BaseTask

class QQBBSearch(BaseTask):
    abstract = False
    name = 'octopus.tasks.qqbb_search'

    def build_args(self, **kwargs):
        return ['scrapy', 'crawl', 'qqbb']


app.register_task(QQBBSearch())

