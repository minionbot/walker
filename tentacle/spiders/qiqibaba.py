# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals
import scrapy
import itertools

from octopus.collect.models import QQBBInstance
from tentacle.items import QQBBInstanceItem
from scrapy_splash import SplashRequest

from cached_property import cached_property

KEYS = [
    '',
]

"""
    't3', '户县',
    't4', '大庆',
    't5', '大寨',
    't11', '韶山',
    't74', '辽塑',
    't82', '西厢',
    't84', '黄帝陵',
    't89', '簪花仕女图',
    't89m',
    't96', '拙政园',
    't99', '牡丹亭',
    't99m',
    't100', '峨眉山',
    't103', '梅花', '梅园',
    't103m',
    't104', '花灯',
    't108', '航天',
    't110', '白鹤',
    't110m',
    't116', '壁画', '敦煌',
    't121', '名楼',
    't129', '兰花',
    't130', '泰山',
    't131', '三国',
    't132', '麋鹿',
    't137', '儿童生活',
    't138', '水浒',
    't140', '华山',
    't141', '美术作品',
    't143', '火箭',
    't144', '西湖',
    't150',
    't151', '铜马车',
    't155', '衡山',
    't156', '都江堰',
    't158', '夜宴图',
    't162', '杜鹃',
    't163', '衡山',
    't164', '避暑山庄', '承德'
    't166', '瓷器', '景德镇',
    't167',
"""

TYPES = [
    '原地 寄',
    '原地封',
    '首日 寄',
]

SEARCHES = itertools.product(KEYS, TYPES)

class QiQiBaBaSpider(scrapy.Spider):
    name = 'qqbb'

    def __init__(self, mode = 'update', **kwargs):
        self.mode = mode
        super(QiQiBaBaSpider).__init__(**kwargs)

    def start_requests(self):
        requests = []
        for word in SEARCHES:
            search = ' '.join(word)
            requests.extend([
                self.get_request(search, 1),
            ])

        return requests

    @cached_property
    def imported_instances(self):
        return QQBBInstance.objects.values_list('source_id', flat = True).order_by('-source_id')

    def get_request(self, key, page):
        return scrapy.FormRequest(
            "https://m.997788.com/all_3/3/164/?d=164&r=&v1=62997&v2=&v3=&v4=&v5=&v6=63008&v7=&v8=&v9=&v10=&v11=&v12=&"
            "t2=0&t4=0&t5=2&t6=&t7=0&t8=0&t9=0&t10=&z=0&p=0&v=0&u=1&y=2&o=o&s0=%s" % key,
            meta = {
                'page': int(page),
                'search': str(key)
            },
            method = 'GET',
            cookies = {'h5_localstorage': 'null'}
        )

    def parse(self, response):
        print(response.request.headers.get('User-Agent'))
        print(response, response.body)
        return {}
