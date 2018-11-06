# -*- coding: utf-8 -*-
from __future__ import division
from datetime import datetime
import re
import scrapy
from django.core.exceptions import ObjectDoesNotExist
from octopus.main.models import StampGroupCatalog, StampSingleCatalog

class ChinesestampSpider(scrapy.Spider):
    name = 'ybb'
    allowed_domains = ['www.china-ybb.com']
    start_urls = [
        'http://www.china-ybb.com/list/4k',
        'http://www.china-ybb.com/list/4h',
        'http://www.china-ybb.com/list/4q',
        'http://www.china-ybb.com/list/4r',
        'http://www.china-ybb.com/list/4a',
        'http://www.china-ybb.com/list/4b',
        'http://www.china-ybb.com/list/4d',
        'http://www.china-ybb.com/list/4l',

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
        self.logger.info("scraping %s", url)

        # has more page
        if index + 1 < len(pages):
            yield scrapy.Request(self.next_page(url, pages[index + 1]), callback = self.parse)

        self.logger.info("processing %s", response.request.url)
        catalogs = response.css('body>div#mulu>div.mr>div.dl')

        for catalog in catalogs:
            self.logger.debug("catalog: %s", catalog)

            title_fields = catalog.css('div.dd>div.ddt>div.l>p::text').extract_first().split('|')
            refs = catalog.css('div.dd>ul>li>a::attr(href)').extract()

            official, name, num, year = map(lambda x: x.strip(), title_fields)
            name = name.strip()

            self.logger.info("fetched [%s][%s]" % (official, name))

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
                self.logger.info("will fetch single item: %s", ref)
                yield scrapy.Request(self.url_prefix + ref,
                                     callback = self.process_single,
                                     meta = {'group': group})

        yield {}

    def is_old_face(self, official):
        v = re.findall(r'\d+', official)
        official = str(official)

        if official.startswith('普东') or official.startswith('普旅') or \
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
        title_fields = response.css('body>div#byc>div#ml>div#mlt>div#mltl>div#h2').extract()[0]
        name_serial = title_fields.split('<br>')[0]
        self.logger.debug("name_serial: %s" % name_serial)

        group = response.request.meta["group"]

        fields = re.findall(r"（(\d+-\d+)）", name_serial)
        sequence = int(fields[0].split('-')[1])

        # self.logger.info("processing %s" % fields[0])

        item = {
            'reference': response.request.url,
            'image_url': self.url_prefix + '/' +
                         response.css('body>div#byc div#pic>.zoom-section a::attr(href)').extract_first()
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
                v = re.findall(r"\d+\.?\d+", attr)
                if not self.is_old_face(group.official):
                    item['face_value'] = float(v[0]) * 100
                else:
                    item['face_value'] = float(v[0])
            if attr.startswith(pub_prefix):
                v = re.findall(r"\d+\.\d+", attr)
                item['pub_number'] = float(v[0]) / 10
            if attr.startswith(pub_date_prefix):
                v = attr.lstrip(pub_date_prefix).strip()
                item['pub_date'] = datetime.strptime(v, '%Y年%m月%d日')
            if attr.startswith(p_prefix):
                v = re.findall(r"\d+\.?\d+", attr)
                item['p'] = float(v[0])
            if attr.startswith(size_prefix):
                v = re.findall(r"(\d+\.?\d+)\*(\d+\.?\d+)", attr)
                item['top_size'] = float(v[0][0])
                item['right_size'] = float(v[0][1])

        single, _ = StampSingleCatalog.objects.update_or_create(
            group = group,
            sequence = sequence,
            defaults = item
        )

        return {}