# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db import models
from polymorphic.models import PolymorphicModel
from octopus.main.models.base import BaseModel

class BaseInstance(BaseModel, PolymorphicModel):

    name = models.CharField(
        '商品名称',
        max_length = 256,
    )

    price = models.FloatField(
        '价格',
        default = 0.0
    )

    image_url = models.URLField(
        default = '',
    )

    reference = models.URLField(
        '来源',
        blank = True,
    )

    put_on_date = models.DateTimeField(
        '上架时间',
        null = True
    )

    watching = models.BooleanField(
        '关注',
        default = False
    )

    search_key = models.CharField(
        '检索词',
        default = '',
        max_length = 64,
    )

    next_query_date = models.DateField(
        '下一次检索日期',
        default = None,
    )


SELL_PREVIEW = '预览中'
SELL_AUCTION = '拍卖中'
SELL_SELLING = '出售中'
SELL_ENDED = '已结束'
SELL_TYPES = (
    (SELL_PREVIEW, SELL_PREVIEW),
    (SELL_AUCTION, SELL_AUCTION),
    (SELL_SELLING, SELL_SELLING),
    (SELL_ENDED, SELL_ENDED),
)

class AuctionMixin(models.Model):

    source_id = models.BigIntegerField(
        '源站拍卖ID',
        unique = True,
    )

    is_auction = models.BooleanField(
        '是否拍卖',
        default = False,
    )

    stage = models.CharField(
        choices = SELL_TYPES,
        default = SELL_AUCTION,
        max_length = 16,
    )

    begin_time = models.DateTimeField(
        '开始时间',
        null = True,
        default = None,
    )

    end_time = models.DateTimeField(
        '结束时间',
        null = True,
        default = None,
    )

    bid_time = models.IntegerField(
        '参拍次数',
        default = 0,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '({}) {}'.format(self.price, self.name)

class KongfzInstance(BaseInstance, AuctionMixin):

    shop_id = models.BigIntegerField(
        '商店ID',
        default = 0,
    )

    class Meta:
        verbose_name_plural = '空夫子列表'
        ordering = ['-put_on_date']

class ZhaoInstance(BaseInstance, AuctionMixin):

    item_id = models.BigIntegerField(
        '赵涌内部ID',
        default = 0,
    )

    class Meta:
        verbose_name_plural = '赵勇列表'
        ordering = ['begin_time']
        unique_together = (('item_id', 'source_id'),)

class QQBBInstance(BaseInstance, AuctionMixin):

    shop_id = models.BigIntegerField(
        '商店ID',
        default = 0,
    )
    
    class Meta:
        verbose_name_plural = '七七八八'
        ordering = ['-put_on_date']
