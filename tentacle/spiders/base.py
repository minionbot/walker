# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import scrapy

from scrapy_splash import SplashFormRequest as BasicSplashFormRequest
from scrapy_splash import SplashRequest

class BaseSpider(scrapy.Spider):
    model = None
    ids = set()

    def imported_instances(self):
        if len(self.ids) > 0:
            return self.ids

        self.ids = set(self.model.objects.values_list('source_id', flat = True).order_by('-source_id'))
        return self.ids

class SplashFormRequest(BasicSplashFormRequest):

    def __init__(self, url=None, callback=None, method=None, formdata=None,
                 body=None, **kwargs):
        # First init FormRequest to get url, body and method
        if formdata:
            scrapy.FormRequest.__init__(
                self, url=url, method=method, formdata=formdata, **kwargs)
            url, method, body = self.url, self.method, self.body
        # Then pass all other kwargs to SplashRequest
        SplashRequest.__init__(
            self, url=url, callback=callback, method=method, body=body,
            **kwargs)