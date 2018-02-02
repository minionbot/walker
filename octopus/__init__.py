import os
import sys

from .setup import prepare_env, MODE

__version__ = '0.1.0'

def manage():
    prepare_env()
    from django.core.management import execute_from_command_line

    if len(sys.argv) >= 2 and sys.argv[1] in ('version', '--version'):
        sys.stdout.write('%s\n' % __version__)
    else:
        execute_from_command_line(sys.argv)

def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "octopus.settings.%s" % MODE)

    import django
    django.setup()
