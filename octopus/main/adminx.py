from django.contrib import admin

# Register your models here.
from .models import StampCatalog

import xadmin

def get_model_fields(cls):
    fields = [f.name for f in cls._meta.get_fields() if f.editable]
    if 'description' in fields:
        fields.remove('description')
        fields.append('description')
    return fields

class StampCatalogAdmin(object):
    fields = get_model_fields(StampCatalog)
    list_display = ("name", "official", "group_num", "sequence", "pub_date", "period")


xadmin.site.register(StampCatalog, StampCatalogAdmin)
