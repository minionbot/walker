from django.contrib import admin
from django.utils.html import format_html_join, format_html

# Register your models here.
from .models import StampGroupCatalog

import xadmin

def get_model_fields(cls):
    fields = [f.name for f in cls._meta.get_fields() if f.editable]
    if 'description' in fields:
        fields.remove('description')
        fields.append('description')
    return fields

class StampCatalogAdmin(object):
    fields = get_model_fields(StampGroupCatalog)
    list_display = ("official", "name", "sequence_name", "image")

    def sequence_name(self, obj):
        return format_html_join("\n",
                                "<span>{} {} {}分</span><br>",
                                ((i.sequence, i.sequence_name, i.face_value)
                                    for i in obj.items.all()))
    sequence_name.short_description = '单枚'

    def image(self, obj):
        return format_html("<img src='{}' width='160' />".format(obj.image_url))
    image.short_description = '缩略图'


xadmin.site.register(StampGroupCatalog, StampCatalogAdmin)
