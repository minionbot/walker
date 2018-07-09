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
            pass

app = Celery('octopus.tasks')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'search-zhao-every-one-hour': {
        'task': 'octopus.tasks.zhao_search',
        'schedule': 60.0 * 60,
        'args': ()
    },
    'search-qqbb-every-one-hour': {
        'task': 'octopus.tasks.qqbb_search',
        'schedule': 60.0 * 60,
        'args': ()
    },
    'watch-zhao-auction-every-15-minute': {
        'task': 'octopus.tasks.zhao_auction_watcher',
        'schedule': 60.0 * 15,
        'args': ()
    }
}

@app.task(bind=True)
def debug_task(self):
    logger.info("!!!Debug Task!!!")
    logger.debug('Requests:{0!r}'.format(self.request))
