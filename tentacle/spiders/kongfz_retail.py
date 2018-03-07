# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import json

import scrapy

from django.utils.timezone import datetime
from octopus.collect.models import KongfzInstance, SELL_ENDED, SELL_SELLING

class KongfzRetailSpider(scrapy.Spider):
    name = 'kongfz_retail'
    root = 'https://app.kongfz.com/invokeSeller/app/item/getItemInfo'

    def __init__(self, shop_id, source_id, **kwargs):
        self.shop_id = shop_id
        self.source_id = source_id
        super(KongfzRetailSpider).__init__(**kwargs)

    def start_requests(self):
        try:
            instance = KongfzInstance.objects.get(
                source_id = self.source_id,
                shop_id = self.shop_id,
                next_query_date = datetime.today()
            )
            if instance.stage == SELL_ENDED:
                return {}
        except KongfzInstance.DoesNotExist:
            pass

        return [scrapy.FormRequest(
            url = self.root,
            formdata = {
                'UserAgent': 'IOS_KFZ_COM_2.0.7_iPhone 7 Plus_10.3.3',
                'itemId': str(self.source_id),
                'shopId': str(self.shop_id),
                'userId': str(8149814),
            }
        )]

    def parse(self, response):
        body = json.loads(response.body_as_unicode())

        instance = KongfzInstance.objects.get(source_id = self.source_id)
        instance.stage = SELL_SELLING if body['sold'] == 0 else SELL_ENDED
        instance.price = body['price']
        instance.reference = body['url'] if body['url'].strip() else instance.reference

        instance.save(update_fields = ['stage', 'price', 'reference'])

        return {
            'sold': body['sold'],
            'price': body['price'],
            'reference': instance.reference
        }


