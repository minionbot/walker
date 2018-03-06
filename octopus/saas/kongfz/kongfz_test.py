# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from octopus.saas.kongfz import KongfzAPI

client = KongfzAPI()


client.item().post(data = {
    'UserAgent':	'IOS_KFZ_COM_2.0.7_iPhone 7 Plus_10.3.3',
    'itemId':	30689838,
    'shopId':	1019427,
    'userId':	8149814
})
