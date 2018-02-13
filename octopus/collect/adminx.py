# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from django.contrib import admin
from django.utils.html import format_html_join, format_html

# Register your models here.
from .models import KongfzInstance

import xadmin

class KongfzInstanceAdmin(object):

    list_display = ('name', 'price', 'date', 'image')

    def image(self, obj):
        return format_html("<a href='{}' target='_blank'><img src='{}' width='160' /></a>".format(
            obj.reference,
            obj.image_url)
        )
    image.short_description = '缩略图'

    def date(self, obj):
        return obj.put_on_date.strftime("%y-%m-%d")
    date.short_description = '上架时间'


xadmin.site.register(KongfzInstance, KongfzInstanceAdmin)
