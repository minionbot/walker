# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from libsaas.services import base
from libsaas.executors.requests_executor import use

from . import item

class KongfzAPI(base.Resource):

    apiroot = "https://app.kongfz.com"

    def __init__(self, parent = None):
        use(verify = False)
        super(KongfzAPI, self).__init__(parent)

    def get_url(self):
        return self.apiroot

    @base.resource(item.Item)
    def item(self):
        return item.Item(self)
