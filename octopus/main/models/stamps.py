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
        max_length = 64,
        blank = True,
        default = ''
    )

    official = models.CharField(
        '官方志号',
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

    sequence_name = models.CharField(
        '序号名称',
        max_length = 32,
        blank = True,
    )

    face_value = models.IntegerField(
        '面值/分',
        default = 20
    )

    pub_date = models.DateField(
        '发行日期',
        default = None
    )

    pub_number = models.FloatField(
        '发行量/万'
    )

    period = models.CharField(
        '年代分类',
        choices = PERIODS,
        max_length = 16,
        blank = True,
        editable = False
    )

    gibbons = models.CharField(
        '吉本斯序号',
        max_length = 16,
        blank = True,
        default = ''
    )

    scott = models.CharField(
        '斯科特序号',
        max_length = 16,
        blank = True,
        default = ''
    )

    michael = models.CharField(
        '米歇尔序号',
        max_length = 16,
        blank = True,
        default = ''
    )

    country = models.CharField(
        '发行国家',
        max_length = 16,
        default = 'CN'
    )

    gum = models.BooleanField(
        '是否有背胶',
        default = True
    )

    image_url = models.URLField(
        blank = True,
        editable = False,
    )

    # print_method = models.CharField(
    #    max_length = 16,
    #    choices = PRINT_CHOICES
    # )

    class Meta:
        unique_together = ('official', 'sequence')

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
