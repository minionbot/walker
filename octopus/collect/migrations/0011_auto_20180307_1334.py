# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-07 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0010_auto_20180306_2110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zhaoinstance',
            options={'ordering': ['begin_time'], 'verbose_name_plural': '赵勇列表'},
        ),
        migrations.AddField(
            model_name='qqbbinstance',
            name='shop_id',
            field=models.BigIntegerField(default=0, verbose_name='商店ID'),
        ),
    ]
