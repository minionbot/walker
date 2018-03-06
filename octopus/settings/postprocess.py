# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

import sys
import logging
import os

if 'celeryd' in sys.argv:
    SQL_DEBUG = False

COMMON_LOG_LEVEL = logging.DEBUG if DEBUG is True else logging.INFO
# main日志默认保存30天，按照每小时切分
LOGBACKUP_HOUR = 24 * 30
# celery日志默认保存30天，按照天级切分
LOGBACKUP_DAY = 30

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {'()': 'octopus.main.compat.RequireDebugFalse'},
        'require_debug_true': {'()': 'octopus.main.compat.RequireDebugTrue'},
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s] [%(process)d] [%(thread)d] : %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)-8s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'main_handler': {
            'level': COMMON_LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'main.log'),
            'when': 'H',
            'backupCount': LOGBACKUP_HOUR,
            'formatter': 'verbose'
        },
        'celery_handler': {
            'level': COMMON_LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, 'celery.log'),
            'when': 'midnight',
            'backupCount': LOGBACKUP_DAY,
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
    'loggers': {
        'django': {
            'handlers': []
        },
        'django.request': {
            'handlers': [
                'console',
                'main_handler'
            ],
            'level': 'WARNING',
            'propagate': False
        },
        'py.warnings': {
            'handlers': ['console']
        },
        'octopus.tasks': {
            'handlers': ['celery_handler'],
            'level': COMMON_LOG_LEVEL,
            'propagate': True
        },
        'celery': {
            'handlers': ['console', 'celery_handler'],
            'level': COMMON_LOG_LEVEL,
            'propagate': True
        },
        'scrapy': {
            'handlers': ['console', 'sentry'],
            'level': COMMON_LOG_LEVEL,
            'propagate': True
        },
    }
}
