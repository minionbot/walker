# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-08 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0013_auto_20180308_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinstance',
            name='name',
            field=models.CharField(max_length=512, verbose_name='商品名称'),
        ),
    ]
