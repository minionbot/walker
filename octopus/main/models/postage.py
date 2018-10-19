# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)
from __future__ import unicode_literals

DEST_TYPE_DOMESTIC = 1
DEST_TYPE_INTERNAL = 2
DEST_TYPE_PACIFIC = 3

DEST_TYPE_HM = 4
DEST_TYPE_HMT = 5

DEST_TYPE_GROUP1 = 6
DEST_TYPE_GROUP2 = 7
DEST_TYPE_GROUP3 = 8

DEST_TYPES = (
    # 77 年后采用
    (DEST_TYPE_DOMESTIC, "国内"),
    (DEST_TYPE_INTERNAL, "国际"),
    (DEST_TYPE_PACIFIC, "亚太"),

    # 86.6.1 后港澳资费
    (DEST_TYPE_HM, "港澳"),

    # 87.11.1 后港澳资费
    (DEST_TYPE_HMT, "港澳台"),

)

class PostageBase(object):
    # "计数资费"
    postage = 0

    # 首日
    begin = None

    # 尾日
    end = None

    # 可累加
    accumulatable = False

    # 目的地
    dest_type = None

class PrintPostage(PostageBase):
    accumulatable = True

class MailPostage(PostageBase):
    accumulatable = True

class BlindPostage(PostageBase):
    accumulatable = True

class PostCardPostage(PostageBase):
    accumulatable = False

class AerogramPostage(PostageBase):
    accumulatable = False

class FastMailPostage(PostageBase):
    accumulatable = True

class RegisterExtra(PostageBase):
    accumulatable = False

class AirExtra(PostageBase):
    accumulatable = True

class ReceiptExtra(PostageBase):
    accumulatable = False

