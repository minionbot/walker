# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from django.apps import AppConfig as BasicAppConfig

class AppConfig(BasicAppConfig):
    name = 'octopus.collect'

    def ready(self):
        from octopus.collect import signals