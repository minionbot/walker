# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'octopus_offline',
        'USER': 'octopus_w',
        'PASSWORD': 'octopus_offline',
        'HOST': '10.6.131.78',
        'PORT': '9306',
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'charset': 'utf8',
            'init_command': 'SET '
                            'storage_engine=INNODB,'
                            'character_set_connection=utf8,'
                            'collation_connection=utf8_bin'
        }
    },
}
