# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-13 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0002_baseinstance_reference'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kongfzinstance',
            options={'verbose_name_plural': '孔夫子列表'},
        ),
        migrations.AddField(
            model_name='baseinstance',
            name='put_on_date',
            field=models.DateTimeField(null=True, verbose_name='上架时间'),
        ),
    ]
