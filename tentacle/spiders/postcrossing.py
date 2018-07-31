# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals, division

from functools import cmp_to_key

from scrapy.spiders import BaseSpider

import json

class PostCrossingSpider(BaseSpider):
    name = 'pt'

    start_urls = ['https://www.postcrossing.com/explore/countries']

    def parse(self, response):
        rows = response.css('table#countryList tr')

        infos = []

        for i, r in enumerate(rows):
            if i == 0:
                continue
            contry = r.css('td')[1].css('a::text').extract_first()
            member = r.css('td')[2].css('*::text').extract_first().strip()
            postcard = r.css('td')[3].css('*::text').extract_first().strip()
            populate = r.css('td')[4].css('*::text').extract_first().strip()

            member = int(str(member).replace(',', ''))
            postcard = int(str(postcard).replace(',', ''))
            populate = int(str(populate).replace(',', ''))

            if populate == 0:
                continue

            percent = (postcard / populate) * 10000

            infos.append({
                'contry': contry,
                'member': member,
                'postcard': postcard,
                'populate': populate,
                'percent': percent
            })

        def compare_card_per_person(a, b):
            if a['postcard'] / a['populate'] > b['postcard'] / b['populate']:
                return 1
            else:
                return -1

        print(json.dumps(sorted(infos, key=cmp_to_key(compare_card_per_person)), indent = 4))

