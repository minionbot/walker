# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-04 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(blank=True, default='')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('is_envelope', models.BooleanField(default=True, verbose_name='是否是实寄')),
                ('canceled_time', models.DateTimeField(default=None, verbose_name='消戳日期')),
                ('has_landing_stamp', models.BooleanField(default=True, verbose_name='是否有落地戳')),
                ('purchase_price', models.FloatField(verbose_name='购买价格')),
                ('purchase_source', models.CharField(choices=[('淘宝', '淘宝'), ('7788', '7788'), ('孔夫子', '孔夫子'), ('快乐网', '快乐网')], default='淘宝', max_length=16, verbose_name='购买来源')),
                ('purchase_date', models.DateTimeField(verbose_name='购买日期')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoverBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(blank=True, default='')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('is_head_offical', models.BooleanField(default=False, verbose_name='总公司封')),
                ('is_branch_offical', models.BooleanField(default=False, verbose_name='分公司封')),
                ('branch_offical_name', models.BooleanField(default='', verbose_name='分公司名称')),
                ('official', models.CharField(max_length=32, verbose_name='官方发行志号')),
                ('is_unofficial', models.BooleanField(default=False, verbose_name='自制封')),
                ('is_unofficial_offical_mail', models.BooleanField(default=False, verbose_name='自制公函封')),
                ('is_natural', models.BooleanField(default=False, verbose_name='自然封')),
                ('is_fdc', models.BooleanField(default=True, verbose_name='是否是首日')),
                ('is_original_local', models.BooleanField(default=False, verbose_name='是否是原地')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoverStampCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('cover_catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Cover')),
            ],
        ),
        migrations.CreateModel(
            name='Stamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(blank=True, default='')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('is_canceled', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=1)),
                ('postmark', models.CharField(choices=[('日戳', '日戳'), ('纪念戳', '纪念戳'), ('火车戳', '火车戳'), ('流动邮局', '流动邮局'), ('轮船戳', '轮船戳'), ('双文字', '双文字')], default='日戳', max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StampCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(default=None, editable=False)),
                ('description', models.TextField(blank=True, default='')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('name_eng', models.CharField(max_length=64, verbose_name='英文名称')),
                ('official', models.CharField(max_length=32, verbose_name='官方发行志号')),
                ('group_num', models.SmallIntegerField(default=1, verbose_name='套内票数')),
                ('sequence', models.SmallIntegerField(default=1, verbose_name='套内序号')),
                ('gibbons', models.CharField(max_length=16, verbose_name='吉本斯序号')),
                ('scott', models.CharField(max_length=16, verbose_name='斯科特序号')),
                ('michael', models.CharField(max_length=16, verbose_name='米歇尔序号')),
                ('country', models.CharField(default='CN', max_length=16, verbose_name='发行国家')),
                ('pub_date', models.DateField(default=None, verbose_name='发行日期')),
                ('gum', models.BooleanField(default=True, verbose_name='有无出厂背胶')),
                ('print_method', models.CharField(choices=[('lithography', 'lithography'), ('letterpress', 'letterpress'), ('letterpress', 'letterpress'), ('lithography', 'lithography')], max_length=16)),
                ('period', models.CharField(choices=[('纪特', '纪特'), ('文革', '文革'), ('编号', '编号'), ('JT', 'JT'), ('编年', '编年')], max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoverCatalog',
            fields=[
                ('coverbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.CoverBase')),
                ('postmark_type', models.CharField(choices=[('日戳', '日戳'), ('纪念戳', '纪念戳'), ('火车戳', '火车戳'), ('流动邮局', '流动邮局'), ('轮船戳', '轮船戳'), ('双文字', '双文字')], default='日戳', max_length=16)),
                ('stamp_catalog', models.ManyToManyField(default=None, to='main.StampCatalog')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.coverbase',),
        ),
        migrations.CreateModel(
            name='PostageCardCatalog',
            fields=[
                ('coverbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.CoverBase')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.coverbase',),
        ),
        migrations.CreateModel(
            name='PostageCoverCatalog',
            fields=[
                ('coverbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.CoverBase')),
                ('type', models.CharField(choices=[('纪念封', '纪念封'), ('普通封', '普通封'), ('普美封', '普美封'), ('美术封', '美术封'), ('专用封', '专用封'), ('礼仪封', '礼仪封')], max_length=16)),
            ],
            options={
                'abstract': False,
            },
            bases=('main.coverbase',),
        ),
        migrations.CreateModel(
            name='PostCardCatalog',
            fields=[
                ('coverbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.CoverBase')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.coverbase',),
        ),
        migrations.AddField(
            model_name='stamp',
            name='catalog',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.StampCatalog'),
        ),
        migrations.AddField(
            model_name='coverstampcatalog',
            name='stamp_catalog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.StampCatalog'),
        ),
        migrations.AddField(
            model_name='coverbase',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_main.coverbase_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='cover',
            name='unoffical_stamps',
            field=models.ManyToManyField(default=None, through='main.CoverStampCatalog', to='main.StampCatalog'),
        ),
        migrations.AddField(
            model_name='cover',
            name='catalog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.CoverCatalog'),
        ),
    ]
