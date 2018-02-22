# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

try:
    from django.utils.log import RequireDebugTrue
except ImportError:
    import logging
    from django.conf import settings

    class RequireDebugTrue(logging.Filter):

        def filter(self, record):
            return settings.DEBUG

try:
    from django.utils.log import RequireDebugFalse
except ImportError:
    class RequireDebugFalse(logging.Filter):
        def filter(self, record):
            return not settings.DEBUG