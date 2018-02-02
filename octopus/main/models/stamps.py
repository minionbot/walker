# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db import models
from .base import BaseModel

PRINT_LITHOGRAPHY = 'lithography'
PRINT_LETTERPRESS = 'letterpress'
PRINT_PHOTOGRAVURE = 'photogravure' #影写版
PRINT_ENGRAVING = 'engraving' # 雕刻版

PRINT_CHOICES = (
    (PRINT_LITHOGRAPHY, PRINT_LITHOGRAPHY),
    (PRINT_LETTERPRESS, PRINT_LETTERPRESS),
    (PRINT_LETTERPRESS, PRINT_LETTERPRESS),
    (PRINT_LITHOGRAPHY, PRINT_LITHOGRAPHY),
)

class Catalog(BaseModel):

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
        '发行日期'
    )

    gum = models.BooleanField(
        '有无出厂背胶',
        default = True
    )

    print_method = models.CharField(
        max_length = 16,
        choices = PRINT_CHOICES
    )