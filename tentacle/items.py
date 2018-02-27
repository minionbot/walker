# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from octopus.setup import prepare_env
prepare_env()

import django
django.setup()

from scrapy_djangoitem import DjangoItem
from octopus.main.models.stamps import StampGroupCatalog, StampSingleCatalog
from octopus.collect.models import KongfzInstance, ZhaoInstance, QQBBInstance

class StampGroupCatalogItem(DjangoItem):
    django_model = StampGroupCatalog

class StampSingleCatalogItem(DjangoItem):
    django_model = StampSingleCatalog

class KongfzInstanceItem(DjangoItem):
    django_model = KongfzInstance

class ZhaoInstanceItem(DjangoItem):
    django_model = ZhaoInstance

class QQBBInstanceItem(DjangoItem):
    django_model = QQBBInstance
