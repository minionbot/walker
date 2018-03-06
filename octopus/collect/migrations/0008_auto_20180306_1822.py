# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 10:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0007_auto_20180223_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='QQBBInstance',
            fields=[
                ('baseinstance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='collect.BaseInstance')),
                ('source_id', models.BigIntegerField(unique=True, verbose_name='源站拍卖ID')),
                ('is_auction', models.BooleanField(default=False, verbose_name='是否拍卖')),
                ('stage', models.CharField(choices=[('预览中', '预览中'), ('拍卖中', '拍卖中'), ('出售中', '出售中'), ('已结束', '已结束')], default='拍卖中', max_length=16)),
                ('begin_time', models.DateTimeField(default=None, null=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(default=None, null=True, verbose_name='结束时间')),
                ('bid_time', models.IntegerField(default=0, verbose_name='参拍次数')),
            ],
            options={
                'verbose_name_plural': '七七八八',
                'ordering': ['-put_on_date'],
            },
            bases=('collect.baseinstance', models.Model),
        ),
        migrations.AddField(
            model_name='baseinstance',
            name='search_key',
            field=models.CharField(default='', max_length=64, verbose_name='检索词'),
        ),
        migrations.AddField(
            model_name='baseinstance',
            name='watching',
            field=models.BooleanField(default=False, verbose_name='关注'),
        ),
        migrations.AddField(
            model_name='kongfzinstance',
            name='begin_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='开始时间'),
        ),
        migrations.AddField(
            model_name='kongfzinstance',
            name='bid_time',
            field=models.IntegerField(default=0, verbose_name='参拍次数'),
        ),
        migrations.AddField(
            model_name='kongfzinstance',
            name='end_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='结束时间'),
        ),
        migrations.AddField(
            model_name='kongfzinstance',
            name='shop_id',
            field=models.BigIntegerField(default=0, verbose_name='商店ID'),
        ),
        migrations.AddField(
            model_name='zhaoinstance',
            name='begin_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='开始时间'),
        ),
        migrations.AddField(
            model_name='zhaoinstance',
            name='bid_time',
            field=models.IntegerField(default=0, verbose_name='参拍次数'),
        ),
        migrations.AddField(
            model_name='zhaoinstance',
            name='end_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='结束时间'),
        ),
        migrations.AddField(
            model_name='zhaoinstance',
            name='item_id',
            field=models.BigIntegerField(default=0, verbose_name='赵涌内部ID'),
        ),
        migrations.AlterField(
            model_name='kongfzinstance',
            name='source_id',
            field=models.BigIntegerField(unique=True, verbose_name='源站拍卖ID'),
        ),
        migrations.AlterField(
            model_name='kongfzinstance',
            name='stage',
            field=models.CharField(choices=[('预览中', '预览中'), ('拍卖中', '拍卖中'), ('出售中', '出售中'), ('已结束', '已结束')], default='拍卖中', max_length=16),
        ),
        migrations.AlterField(
            model_name='zhaoinstance',
            name='source_id',
            field=models.BigIntegerField(unique=True, verbose_name='源站拍卖ID'),
        ),
        migrations.AlterField(
            model_name='zhaoinstance',
            name='stage',
            field=models.CharField(choices=[('预览中', '预览中'), ('拍卖中', '拍卖中'), ('出售中', '出售中'), ('已结束', '已结束')], default='拍卖中', max_length=16),
        ),
    ]