# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from polymorphic.models import PolymorphicModel
from django.db import models

from .const import CONDITION, USAGE

class BasePrice(PolymorphicModel):

    price = models.FloatField(
        "价格"
    )

    date = models.DateTimeField(
        "价格日期"
    )

    usage = models.CharField(
        choices = USAGE,
        blank = False,
        max_length = 16,
    )

    condition = models.CharField(
        choices = CONDITION,
        blank = False,
        max_length = 16,
    )

class GroupPrice(BasePrice):

    group = models.ForeignKey(
        "StampGroupCatalog",
    )

    class Meta:
        verbose_name_plural = '组价格'

class SinglePrice(BasePrice):

    single = models.ForeignKey(
        "StampSingleCatalog",
    )

    class Meta:
        verbose_name_plural = '单枚价格'
