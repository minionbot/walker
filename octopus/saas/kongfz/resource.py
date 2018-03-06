# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from libsaas.services import base
from libsaas import http, parsers

class KongfzResource(base.RESTResource):
    def __init__(self, parent, object_id=None):
        super(KongfzResource, self).__init__(parent, object_id)

    @base.apimethod
    def post(self, data = None):
        """
        Post data
        """

        request = http.Request('POST', self.get_url(), data, headers = {
            'user-agent': 'IOS_KFZ_COM_2.0.7_iPhone 7 Plus_10.3.3'
        })
        return request, parsers.parse_json

