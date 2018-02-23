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
        max_length = 128,
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


AUCTION_PREVIEW = '预览'
AUCTION_AUCTION = '拍卖中'
AUCTION_ENDED = '结束'
AUCTION_TYPES = (
    (AUCTION_PREVIEW, AUCTION_PREVIEW),
    (AUCTION_AUCTION, AUCTION_AUCTION),
    (AUCTION_ENDED, AUCTION_ENDED),
)

class AuctionMixin(models.Model):

    source_id = models.BigIntegerField(
        '源站ID',
        unique = True,
    )

    is_auction = models.BooleanField(
        '是否拍卖',
        default = False,
    )

    stage = models.CharField(
        choices = AUCTION_TYPES,
        default = AUCTION_AUCTION,
        max_length = 16,
    )

    class Meta:
        abstract = True

class KongfzInstance(BaseInstance, AuctionMixin):

    def __str__(self):
        return '({}) {}'.format(self.price, self.name)

    class Meta:
        verbose_name_plural = '空夫子列表'
        ordering = ['-put_on_date']

class ZhaoInstance(BaseInstance, AuctionMixin):

    def __str__(self):
        return '({}) {}'.format(self.price, self.name)

    class Meta:
        verbose_name_plural = '赵勇列表'
        ordering = ['-put_on_date']
