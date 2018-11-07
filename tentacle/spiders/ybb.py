# -*- coding: utf-8 -*-
from __future__ import division
from datetime import datetime
import re
import scrapy
from octopus.main.models import StampGroupCatalog, StampSingleCatalog

class ChinesestampSpider(scrapy.Spider):
    name = 'ybb'
    allowed_domains = ['www.china-ybb.com']

    start_urls = [
        'http://www.china-ybb.com/list/4k',  # 普
        'http://www.china-ybb.com/list/4h',  # 纪
        'http://www.china-ybb.com/list/4q',  # 特
        'http://www.china-ybb.com/list/4r',  # 文
        'http://www.china-ybb.com/list/4c',  # 编
        'http://www.china-ybb.com/list/4a',  # J
        'http://www.china-ybb.com/list/4b',  # T
        'http://www.china-ybb.com/list/4l',  # 欠改军航包
    ]

    url_prefix = 'http://www.china-ybb.com'

    def next_page(self, url, next):
        fragments = url.split('/')
        fragments[-1] = next

        return '/'.join(fragments)

    def parse(self, response):
        # 获取页码
        pages = response.css('body>div#mulu>div.mrfy>a::attr(href)').extract()
        current_page = response.css('body>div#mulu>div.mrfy>a.active::attr(href)').extract()[0]

        index = pages.index(current_page)
        url = response.request.url
        self.logger.debug("scraping %s", url)

        # has more page
        if index + 1 < len(pages):
            yield scrapy.Request(self.next_page(url, pages[index + 1]), callback = self.parse)

        self.logger.debug("processing %s", response.request.url)

        catalogs = response.css('body>div#mulu>div.mr>div.dl')

        for catalog in catalogs:
            self.logger.debug("catalog: %s", catalog)

            title_fields = catalog.css('div.dd>div.ddt>div.l>p::text').extract_first().split('|')
            refs = catalog.css('div.dd>ul>li>a::attr(href)').extract()

            official, name, num, year = map(lambda x: x.strip(), title_fields)
            if official.startswith('个'):
                continue

            name = name.strip()

            self.logger.debug("fetched [%s][%s]" % (official, name))

            new_keys, old_keys = self.detect_key(catalog.css('div.dd>ul>li>a'))

            defaults = {
                'country': 'CN',
                'period': datetime.strptime(year, '%Y年'),
                'group_num': len(refs),
                'name': name,
            }
            group, _ = StampGroupCatalog.objects.update_or_create(
                official = official,
                defaults = defaults
            )

            for ref in refs:
                self.logger.debug("will fetch single item: %s", ref)
                yield scrapy.Request(self.url_prefix + ref,
                                     callback = self.process_single,
                                     meta = {'group': group, 'new_keys': new_keys, 'old_keys': old_keys})

        yield {}

    def is_old_face(self, official):
        v = re.findall(r'\d+', official)
        official = str(official)

        if official.startswith('普东') or official.startswith('普旅') or official.startswith('普无号') or \
            official.startswith('改') or official.startswith('欠') or \
            official.startswith('航1') or official.startswith('军1'):
            return True

        if official.startswith('普'):
            return 1 <= int(v[0]) <= 7
        if official.startswith('纪'):
            return 1 <= int(v[0]) <= 30
        if official.startswith('特'):
            return 1 <= int(v[0]) <= 12

        return False

    def process_single(self, response):
        url = response.request.url
        title_fields = response.css('body>div#byc>div#ml>div#mlt>div#mltl>div#h2::text').extract_first()
        name_serial = title_fields.split('<br>')[0]

        self.logger.debug("name_serial: %s" % name_serial)

        group = response.request.meta["group"]
        new_keys = response.request.meta["new_keys"]
        old_keys = response.request.meta["old_keys"]

        fields = re.findall(r"（(\d+-\d+)）", name_serial)
        sequence = int(fields[0].split('-')[1])

        item = {
            'reference': response.request.url,
            'image_url': self.url_prefix + '/' +
                         response.css('body>div#byc div#pic>.zoom-section a::attr(href)').extract_first(),
            'price_percent':   new_keys[sequence] if sequence in new_keys else 0.0,
            'old_price_percent':   old_keys[sequence] if sequence in old_keys else 0.0,
        }

        attrs = response.css('body>div#byc>div#mr>ul.b_info')[0].css('li::text').extract()
        for attr in attrs:
            name_prefix = '名称：'
            face_prefix = '面值：'
            pub_prefix = '发行量：'
            pub_date_prefix = '发行日期：'
            p_prefix = '齿孔：'
            size_prefix = '尺寸：'
            if attr.startswith(name_prefix):
                item['sequence_name'] = attr.lstrip(name_prefix).strip()
            if attr.startswith(face_prefix):
                v = re.findall(r"\d+\.?\d*", attr)
                if len(v) == 2:
                    item['old_face_value'] = float(v[-1])
                if not self.is_old_face(group.official):
                    item['face_value'] = float(v[0]) * 100
                else:
                    item['face_value'] = float(v[0])
            if attr.startswith(pub_prefix):
                v = re.findall(r"\d+\.\d+", attr)
                item['pub_number'] = float(v[0]) / 10
            if attr.startswith(pub_date_prefix):
                v = str(attr).lstrip(pub_date_prefix).strip()
                if v.endswith('日'):
                    item['pub_date'] = datetime.strptime(v, '%Y年%m月%d日')
                else:
                    item['pub_date'] = datetime.strptime(v, '%Y年%m月')
            if attr.startswith(p_prefix):
                v = re.findall(r"\d+\.?\d*", attr)
                if len(v):
                    item['p'] = float(v[0])

            if attr.startswith(size_prefix):
                v = re.findall(r"(\d+\.?\d*)\*(\d+\.?\d*)", attr)
                item['top_size'] = float(v[0][0])
                item['right_size'] = float(v[0][1])

        single, _ = StampSingleCatalog.objects.update_or_create(
            group = group,
            sequence = sequence,
            defaults = item
        )

        self.logger.info("processed %s" % name_serial)
        return {}

    def detect_key(self, prices):
        total = 0.0
        old_total = 0.0

        for price in prices:
            fields = price.css('a>font::text').extract()
            self.logger.debug("%s", price)
            if len(fields) > 1:
                total += float(fields[1])
            if len(fields) == 3:
                old_total += float(fields[2])

        new_percent = {}
        old_percent = {}
        for idx, price in enumerate(prices):
            fields = price.css('a>font::text').extract()
            if len(fields) > 1:
                new_percent[idx + 1] = '%0.2f' % (float(fields[1])/total)
            if len(fields) == 3 and old_total != 0.0:
                old_percent[idx + 1] = '%0.2f' % (float(fields[2])/old_total)

        return new_percent, old_percent
