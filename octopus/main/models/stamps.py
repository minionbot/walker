# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db import models
from .base import BaseModel
from .const import *

__all__ = [
    'StampCatalog',
    'Stamp'
]

class StampCatalog(BaseModel):

    name = models.CharField(
        '名称',
        max_length = 64
    )

    name_eng = models.CharField(
        '英文名称',
        max_length = 64
    )

    official = models.CharField(
        '官方发行志号',
        max_length = 32,
    )

    group_num = models.SmallIntegerField(
        '套内票数',
        default = 1
    )

    sequence = models.SmallIntegerField(
        '套内序号',
        default = 1
    )

    gibbons = models.CharField(
        '吉本斯序号',
        max_length = 16,
    )

    scott = models.CharField(
        '斯科特序号',
        max_length = 16,
    )

    michael = models.CharField(
        '米歇尔序号',
        max_length = 16,
    )

    country = models.CharField(
        '发行国家',
        max_length = 16,
        default = 'CN'
    )

    pub_date = models.DateField(
        '发行日期',
        default = None
    )

    gum = models.BooleanField(
        '有无出厂背胶',
        default = True
    )

    print_method = models.CharField(
        max_length = 16,
        choices = PRINT_CHOICES
    )

    period = models.CharField(
        choices = PERIODS,
        max_length = 16,
    )

class Stamp(BaseModel):
    catalog = models.ForeignKey(
        StampCatalog,
        default = None,
        on_delete = models.CASCADE
    )

    is_canceled = models.BooleanField(
        default = False
    )

    count = models.IntegerField(
        default = 1
    )

    postmark = models.CharField(
        choices = MARK_TYPE,
        max_length = 16,
        default = MARK_TYPE_NORMAL
    )
