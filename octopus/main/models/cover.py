# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db import models
from .base import BaseModel

class Cover(BaseModel):

    canceled_time = models.DateTimeField(
        '消戳日期',
        default = None
    )

    is_envelope = models.BooleanField(
        '是否是实寄封',
        default = True
    )

    is_fdc = models.BooleanField(
        '是否是首日封',
    )

    is_original_local = models.BooleanField(
        '是否是原地封',
    )

