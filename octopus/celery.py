# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)
import logging
from octopus.setup import prepare_env, is_dev

prepare_env()

import raven
from raven.contrib.celery import register_signal, register_logger_signal
logger = logging.getLogger('celery')

if is_dev():
    from celery import Celery
else:
    import celery

    class Celery(celery.Celery):
        def on_configure(self):
            client = raven.Client('http://b54e335cd8e047808f07d9ac6711ae70:3d2840c713fe4341bbf70afc6e9faea0@ad.sentry.m.byted.org/260')

            # register a custom filter to filter out duplicate logs
            register_logger_signal(client)

            # hook into the Celery error handler
            register_signal(client)

app = Celery('octopus.tasks')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'search-kongfz-every-one-hour': {
        'task': 'octopus.tasks.kongfz_search',
        'schedule': 60.0 * 60,
        'args': ()
    },
    'search-zhao-every-one-hour': {
        'task': 'octopus.tasks.zhao_search',
        'schedule': 60.0 * 60,
        'args': ()
    },
    'watch-kongfz-every-15-minute': {
        'task': 'octopus.tasks.kongfz_auction_watcher',
        'schedule': 60.0 * 15,
        'args': ()
    }
}

@app.task(bind=True)
def debug_task(self):
    logger.info("!!!Debug Task!!!")
    logger.debug('Requests:{0!r}'.format(self.request))
