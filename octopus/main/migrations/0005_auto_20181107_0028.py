# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-06 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20181107_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='stampsinglecatalog',
            name='old_face_value',
            field=models.IntegerField(default=0, verbose_name='改值原面值'),
        ),
        migrations.AlterField(
            model_name='stampsinglecatalog',
            name='sequence_name',
            field=models.CharField(blank=True, max_length=128, verbose_name='序号名称'),
        ),
    ]
