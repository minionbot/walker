# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import KongfzInstance
from octopus.tasks.notify import send_slack

@receiver(post_save, sender = KongfzInstance)
def notify(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if not created:
        return

    send_slack.delay('#kongfz', instance.name, instance.image_url, instance.reference)

