# coding: utf-8
# Copyright © 2017 All Rights Reserved.
# Wangjing (wangjild@gmail.com)
import warnings
import importlib
import os

__env_names = {'devonly': 'development'}
MODE = 'production'

for env, mode in list(__env_names.items()):
    if MODE != 'production':
        break
    try:
        importlib.import_module('octopus.' + env)
        MODE = mode
    except ImportError:
        pass

def prepare_env():
    print ('octopus.settings.%s' % MODE)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octopus.settings.%s' % MODE)
    from django.conf import settings
    if not settings.DEBUG:
        warnings.simplefilter('ignore', DeprecationWarning)

    import django.core.management
    django.core.management.find_commands = find_commands

    if settings.DEBUG and not getattr(settings, 'SQL_DEBUG', True):
        from django.db.backends.base.base import BaseDatabaseWrapper
        from django.db.backends.utils import CursorWrapper
        BaseDatabaseWrapper.make_debug_cursor = lambda self, cursor: CursorWrapper(cursor, self)

def is_dev():
    return MODE != 'production'

def find_commands(management_dir):
    command_dir = os.path.join(management_dir, 'commands')
    commands = []
    try:
        for f in os.listdir(command_dir):
            if f.startswith('_'):
                continue
            elif f.endswith('.py') and f[:-3] not in commands:
                commands.append(f[:-3])
            elif f.endswith('.pyc') and f[:-4] not in commands:
                commands.append(f[:-4])

    except OSError:
        pass

    return commands

