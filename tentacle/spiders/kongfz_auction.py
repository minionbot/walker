# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import logging

import scrapy
from tentacle.items import KongfzInstanceItem, KongfzInstance
from octopus.collect.models import SELL_ENDED, SELL_AUCTION

from scrapy_splash import SplashRequest

from django.utils.timezone import datetime

logger = logging.getLogger('scrapy')

class KongfzAuctionSpider(scrapy.Spider):
    name = 'kongfz_auction'
    root = 'http://m.kongfz.cn/{auction_id}'

    def __init__(self, auction_id, mode = 'update', **kwargs):
        self.mode = mode
        self.auction_id = auction_id
        super(KongfzAuctionSpider).__init__(**kwargs)

    def start_requests(self):
        return [SplashRequest(url = self.root.format(auction_id = self.auction_id))]

    def parse(self, response):
        state = response.css('nav.kfz-banner .tip.show .f_left .c_white_o7::text').extract_first()
        if state is None:
            state = response.css('nav.kfz-banner .tip.show .f_left .c_white::text').extract_first()

        in_auction = True

        if state == '已结束':
            in_auction = False
        elif not str(state).startswith('剩余'):
            logger.error('got unknow state %s' % state, extra={
                'stack': True,
            })

            return {}

        if in_auction:
            price, bid_time = self.parse_in_auction(response)
        else:
            price, bid_time = self.parse_ended(response)

        group = response.css('section .auction_list_group')[0].css('.list_item .item_right::text').extract()
        item_id, begin_time, end_time = group[0], group[2] + '+0800', group[3] + '+0800'

        instance = KongfzInstance.objects.get(source_id = self.auction_id)
        instance.bid_time = bid_time
        instance.price = price
        instance.begin_time = begin_time
        instance.end_time = end_time
        instance.stage = SELL_AUCTION if in_auction else SELL_ENDED
        instance.save(update_fields = ['bid_time', 'price', 'begin_time', 'end_time', 'stage'])

        return {
            'id': int(item_id),
            'price': price,
            'bid_time': bid_time,
            'in_auction': in_auction,
            'begin_time': begin_time,
            'end_time': end_time,
        }

    def parse_in_auction(self, response):
        bid_times = response.css('section div.auction_head .info.show .info_con.c_gray_9 .con_list')[
            -1].css('.c_gray_3::text').extract_first()
        bid_times = int(bid_times)

        if bid_times > 0:
            price = response.css('section div.auction_head .info.show .state .c_red .price::text').extract_first()
            price = float(price)
        else:
            price = response.css('section div.auction_head .info.show .info_con.c_gray_9 .con_list')[
                0].css('.c_gray_3 span::text').extract_first()
            price = float(price)

        return price, bid_times

    def parse_ended(self, response):
        bid_times = response.css('section div.auction_head .info.end.show .info_con.c_gray_9 .con_list')[
            -1].css('.c_gray_3::text').extract_first()
        bid_times = int(bid_times)

        if bid_times > 0:
            price = response.css('section div.auction_head .info.end.show .state .c_red .price::text').extract_first()
            price = float(price)
        else:
            price = response.css('section div.auction_head .info.end.show .info_con.c_gray_9 .con_list')[
                0].css('.c_gray_3 span::text').extract_first()
            price = float(price)

        return price, bid_times
