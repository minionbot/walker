# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import KongfzInstance, ZhaoInstance, QQBBInstance
from octopus.tasks.notify import send_slack

@receiver(post_save, sender = KongfzInstance)
def kfz_notify(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if not created:
        return

    send_slack.delay('#kongfz', instance.name, instance.image_url, instance.reference, instance.price)

@receiver(post_save, sender = ZhaoInstance)
def zhao_notify(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if not created:
        return

    send_slack.delay('#zhaoonline', instance.name, instance.image_url, instance.reference, instance.price)

@receiver(post_save, sender = QQBBInstance)
def qqbb_notify(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if not created:
        return

    send_slack.delay('#qqbb', instance.name, instance.image_url, instance.reference, instance.price)
