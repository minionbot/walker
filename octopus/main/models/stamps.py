# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db import models
from .base import BaseModel
from .const import *

__all__ = [
    'StampGroupCatalog',
    'StampSingleCatalog',
    'Stamp'
]

class StampSingleCatalog(BaseModel):

    group = models.ForeignKey(
        to = 'StampGroupCatalog',
        on_delete = models.CASCADE,
        related_name = 'items'
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

    pub_number = models.FloatField(
        '发行量/万',
        null = True
    )

    pub_date = models.DateField(
        '发行日期',
        default = None,
        null = True,
    )

    face_value = models.IntegerField(
        '面值/分',
        default = 20
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

    class Meta:
        verbose_name_plural = '单枚目录'


class StampGroupCatalog(BaseModel):

    name = models.CharField(
        '名称',
        max_length = 64
    )

    official = models.CharField(
        '官方志号',
        unique = True,
        max_length = 32,
    )

    group_num = models.SmallIntegerField(
        '套内票数',
        default = 1
    )

    total_face_value = models.IntegerField(
        '面值/分',
        default = 20
    )

    period = models.CharField(
        '年代分类',
        choices = PERIODS,
        max_length = 16,
        blank = True,
        editable = False
    )

    name_eng = models.CharField(
        '英文名称',
        max_length = 64,
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
        default = '',
        blank = True,
        editable = False,
    )

    reference = models.URLField(
        '来源',
        blank = True,
    )

    # print_method = models.CharField(
    #    max_length = 16,
    #    choices = PRINT_CHOICES
    # )

    def __str__(self):
        return '%s - %s' % (self.official, self.name)

    class Meta:
        verbose_name_plural = '套票目录'


class Stamp(BaseModel):
    catalog = models.ForeignKey(
        StampGroupCatalog,
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
