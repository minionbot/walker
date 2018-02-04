# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db import models
from polymorphic.models import PolymorphicModel

from .base import BaseModel
from .const import *

__all__ = [
    'CoverCatalog',
    'CoverStampCatalog',
    'Cover',
]

class CoverBase(BaseModel, PolymorphicModel):

    is_head_offical = models.BooleanField(
        '总公司封',
        default = False,
    )

    is_branch_offical = models.BooleanField(
        '分公司封',
        default = False,
    )

    branch_offical_name = models.BooleanField(
        '分公司名称',
        default = ''
    )

    official = models.CharField(
        '官方发行志号',
        max_length = 32,
    )

    is_unofficial = models.BooleanField(
        '自制封',
        default = False,
    )

    is_unofficial_offical_mail = models.BooleanField(
        '自制公函封',
        default = False,
    )

    is_natural = models.BooleanField(
        '自然封',
        default = False,
    )

    is_fdc = models.BooleanField(
        '是否是首日',
        default = True,
    )

    is_original_local = models.BooleanField(
        '是否是原地',
        default = False,
    )

class CoverCatalog(CoverBase):
    stamp_catalog = models.ManyToManyField(
        'main.StampCatalog',
        default = None
    )

    postmark_type = models.CharField(
        choices = MARK_TYPE,
        default = MARK_TYPE_NORMAL,
        max_length = 16
    )

class CoverStampCatalog(models.Model):
    """
    记录封上的邮票和数目
    """

    stamp_catalog = models.ForeignKey(
        'StampCatalog',
        on_delete = models.CASCADE
    )

    cover_catalog = models.ForeignKey(
        'Cover',
        on_delete = models.CASCADE
    )

    count = models.IntegerField(default = 1)

class Cover(BaseModel):

    catalog = models.ForeignKey(
        CoverCatalog,
    )

    is_envelope = models.BooleanField(
        '是否是实寄',
        default = True
    )

    canceled_time = models.DateTimeField(
        '消戳日期',
        default = None
    )

    has_landing_stamp = models.BooleanField(
        '是否有落地戳',
        default = True
    )

    purchase_price = models.FloatField(
        '购买价格',
    )

    purchase_source = models.CharField(
        '购买来源',
        choices = PURCHASE_SOURCE,
        default = PURCHASE_SOURCE_TB,
        max_length = 16
    )

    purchase_date = models.DateTimeField(
        '购买日期',
    )

    unoffical_stamps = models.ManyToManyField(
        'StampCatalog',
        through = 'CoverStampCatalog',
        default = None
    )

class PostageCoverCatalog(CoverBase):
    type = models.CharField(
        choices = POSTAGE_TYPE,
        max_length = 16,
    )

class PostCardCatalog(CoverBase):
    pass

class PostageCardCatalog(CoverBase):
    pass
