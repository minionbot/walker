# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import os

from django.conf import settings
from octopus.celery import app
from tentacle.proxy import Proxies

@app.task(name = 'octopus.tasks.update_proxies')
def update_proxies(self):
    a = Proxies()
    a.verify_proxies()

    proxie = a.proxies
    datasource = os.path.join(settings.PROJ_DIR, 'tentacle', 'proxies.txt')
    with open(datasource, 'w+') as f:
        for proxy in proxie:
            f.write(proxy + '\n')
