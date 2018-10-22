# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from collections import namedtuple

PURCHASE_SOURCE_TB = '淘宝'
PURCHASE_SOURCE_7788 = '7788'
PURCHASE_SOURCE_KFZ = '孔夫子'
PURCHASE_SOURCE_KL = '快乐网'

PURCHASE_SOURCE = (
    (PURCHASE_SOURCE_TB, PURCHASE_SOURCE_TB),
    (PURCHASE_SOURCE_7788, PURCHASE_SOURCE_7788),
    (PURCHASE_SOURCE_KFZ, PURCHASE_SOURCE_KFZ),
    (PURCHASE_SOURCE_KL, PURCHASE_SOURCE_KL),
)


PRINT_LITHOGRAPHY = 'lithography'
PRINT_LETTERPRESS = 'letterpress'
PRINT_PHOTOGRAVURE = 'photogravure'  # 影写版
PRINT_ENGRAVING = 'engraving'  # 雕刻版

PRINT_CHOICES = (
    (PRINT_LITHOGRAPHY, PRINT_LITHOGRAPHY),
    (PRINT_LETTERPRESS, PRINT_LETTERPRESS),
    (PRINT_LETTERPRESS, PRINT_LETTERPRESS),
    (PRINT_LITHOGRAPHY, PRINT_LITHOGRAPHY),
)

PERIOD_PRC_CS = '纪特'
PERIOD_PRC_RL = '文革'
PERIOD_PRC_NUM = '编号'
PERIOD_PRC_JT = 'JT'
PERIOD_PRC_YEAR = '编年'

PERIODS = (
    (PERIOD_PRC_CS, PERIOD_PRC_CS),
    (PERIOD_PRC_RL, PERIOD_PRC_RL),
    (PERIOD_PRC_NUM, PERIOD_PRC_NUM),
    (PERIOD_PRC_JT, PERIOD_PRC_JT),
    (PERIOD_PRC_YEAR, PERIOD_PRC_YEAR),
)

#  纪念邮戳 风景邮戳 火车邮戳
# 流动邮局邮戳 船舶邮戳 军邮戳 特殊邮戳 地方邮局戳 私人邮政邮戳 双邮戳 双圈邮戳 双文字邮戳 其他邮戳
MARK_TYPE_NORMAL = '日戳'
MARK_TYPE_JN = '纪念戳'
MARK_TYPE_FJ = '风景戳'
MARK_TYPE_HUOCHE = '火车戳'
MARK_TYPE_LIUDONG = '流动邮局'
MARK_TYPE_LUNCHUAN = '轮船戳'
MARK_TYPE_SHUANGWENZI = '双文字'

MARK_TYPE = (
    (MARK_TYPE_NORMAL, MARK_TYPE_NORMAL),
    (MARK_TYPE_JN, MARK_TYPE_JN),
    (MARK_TYPE_HUOCHE, MARK_TYPE_HUOCHE),
    (MARK_TYPE_LIUDONG, MARK_TYPE_LIUDONG),
    (MARK_TYPE_LUNCHUAN, MARK_TYPE_LUNCHUAN),
    (MARK_TYPE_SHUANGWENZI, MARK_TYPE_SHUANGWENZI),
)


POSTAGE_TYPE_JF = '纪念封'
POSTAGE_TYPE_PF = '普通封'
POSTAGE_TYPE_PMF = '普美封'
POSTAGE_TYPE_MF = '美术封'
POSTAGE_TYPE_ZF = '专用封'
POSTAGE_TYPE_LF = '礼仪封'

POSTAGE_TYPE = (
    (POSTAGE_TYPE_JF, POSTAGE_TYPE_JF),
    (POSTAGE_TYPE_PF, POSTAGE_TYPE_PF),
    (POSTAGE_TYPE_PMF, POSTAGE_TYPE_PMF),
    (POSTAGE_TYPE_MF, POSTAGE_TYPE_MF),
    (POSTAGE_TYPE_ZF, POSTAGE_TYPE_ZF),
    (POSTAGE_TYPE_LF, POSTAGE_TYPE_LF),
)

Condition = namedtuple('Condition', ['en', 'cn'])
CONDITION_VF = Condition(en = 'VF', cn = '全品')
CONDITION_FINE = Condition(en = 'F', cn = '上品')
CONDITION_GOOD = Condition(en = 'G', cn = '中上品')
CONDITION_AVG = Condition(en = 'A', cn = '中品')
CONDITION_BAD = Condition(en = 'Bad', cn = '中品')


CONDITION = (
    (CONDITION_VF.en, CONDITION_VF.cn),
    (CONDITION_FINE.en, CONDITION_FINE.cn),
    (CONDITION_GOOD.en, CONDITION_GOOD.cn),
    (CONDITION_AVG.en, CONDITION_AVG.cn),
    (CONDITION_BAD.en, CONDITION_BAD.cn),
)

Usage = namedtuple('Usage', ['en', 'cn'])

USAGE_CTO = Usage(en = 'CTO', cn = '盖销')
USAGE_NEW = Usage(en = 'NEW', cn = '新票')
USAGE_USED = Usage(en = 'USED', cn = '信销')

USAGE = (
    (USAGE_CTO.en, USAGE_CTO.cn),
    (USAGE_NEW.en, USAGE_NEW.cn),
    (USAGE_USED.en, USAGE_USED.cn),
)
