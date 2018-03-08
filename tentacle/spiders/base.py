# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import scrapy

class BaseSpider(scrapy.Spider):
    model = None
    ids = set()

    def imported_instances(self):
        if len(self.ids) > 0:
            return self.ids

        self.ids = set(self.model.objects.values_list('source_id', flat = True).order_by('-source_id'))
        return self.ids
