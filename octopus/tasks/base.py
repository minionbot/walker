# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

import os
import pipes
import shutil
import time
import traceback
import pexpect
import codecs
import uuid

try:
    import psutil
except:
    psutil = None

from django.db import DatabaseError, OperationalError, close_old_connections
from django.conf import settings

from celery import Task
from celery.utils.log import get_logger

from raven.contrib.django.raven_compat.models import client as sentry_client

logger = get_logger('celery')

__all__ = [
    'BaseTask',
]


def retry_if_database_error(exception):
    if isinstance(exception, (OperationalError, DatabaseError)):
        close_old_connections()
        return True
    return False

class BaseTask(Task):
    name = None
    abstract = True

    def signal_finished(self):
        pass

    def get_path_to(self, *args):
        """
        Return absolute path relative to this file.
        """
        return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), *args))

    def debug_env(self):
        if not settings.DEBUG:
            return

        for key, val in os.environ.items():
            print('ENV %s:%s ' % (key, val))

    def prepare_task_env(self):
        pass

    def build_env(self, **kwargs):
        """
        Build environment dictionary for ansible-playbook.
        """
        env = dict(os.environ.items())

        for attr in dir(settings):
            if attr == attr.upper() and attr.startswith('ANSIBLE_'):
                env[attr] = str(getattr(settings, attr))

        python_paths = env.get('PYTHONPATH', '').split(os.pathsep)
        local_site_packages = self.get_path_to('..', 'lib', 'site-packages')
        if local_site_packages not in python_paths:
            python_paths.insert(0, local_site_packages)
        env['PYTHONPATH'] = os.pathsep.join(python_paths)
        env['JOB_STDOUT_FILENAME'] = '%s-%s.out' % (self.name, str(uuid.uuid1()))

        # build python virtualenv path
        value = os.path.join(settings.PROJ_DIR, '.env', 'bin')
        env['PATH'] = os.environ.get('PATH', '/usr/bin') + ':' + value
        return env

    def args2cmdline(self, *args):
        return ' '.join([ pipes.quote(a) for a in args ])

    def get_ssh_key_path(self, **kwargs):
        """
        Return the path to the SSH key file, if present.
        """
        return ''

    def wrap_args_with_ssh_agent(self, args, ssh_key_path, ssh_auth_sock = None):
        if ssh_key_path:
            cmd = ' && '.join([self.args2cmdline('ssh-add', ssh_key_path), self.args2cmdline('rm', '-f', ssh_key_path), self.args2cmdline(*args)])
            args = ['ssh-agent']
            if ssh_auth_sock:
                args.extend(['-a', ssh_auth_sock])
            args.extend(['sh', '-c', cmd])
        return args

    def build_args(self, **kwargs):
        raise NotImplementedError

    def build_cwd(self, **kwargs):
        return settings.PROJ_DIR

    def run_pexpect(self, args, cwd, env, stdout_handle):
        """
        Run the given command using pexpect to capture output and provide
        passwords when requested.
        """

        logfile = stdout_handle
        logfile_pos = logfile.tell()

        child = pexpect.spawnu(args[0], args[1:], cwd=cwd, env=env, maxread = 4096)
        child.logfile_read = logfile
        child.delayafterread = None

        last_stdout_update = time.time()

        expect_list = [pexpect.EOF, pexpect.TIMEOUT]
        expect_passwords = {}
        pexpect_timeout = getattr(settings, 'PEXPECT_TIMEOUT', 5)

        while child.isalive():
            result_id = child.expect(expect_list, timeout=pexpect_timeout)
            if result_id in expect_passwords:
                child.sendline(expect_passwords[result_id])
            if logfile_pos != logfile.tell():
                logfile_pos = logfile.tell()
                last_stdout_update = time.time()

        if child.exitstatus == 0:
            return 'successful', child.exitstatus
        else:
            return 'failed', child.exitstatus

    def pre_run_hook(self, **kwargs):
        """
        Hook for any steps to run before the job/task starts
        """
        pass

    def post_run_hook(self, **kwargs):
        """
        Hook for any steps to run after job/task is complete.
        """
        pass

    def run(self, **kwargs):
        """
        Run the job/task and capture its output.
        """
        status, rc, tb = ('error', None, '')
        try:
            args = self.build_args(**kwargs)
            cwd = self.build_cwd(**kwargs)
            env = self.build_env(**kwargs)

            if not os.path.exists(settings.JOBOUTPUT_ROOT):
                os.makedirs(settings.JOBOUTPUT_ROOT)
            stdout_filename = os.path.join(settings.JOBOUTPUT_ROOT, env['JOB_STDOUT_FILENAME'])

            stdout_handle = codecs.open(stdout_filename, 'w', encoding='utf-8')
            status, rc = self.run_pexpect(args, cwd, env, stdout_handle)
        except Exception:
            if status != 'canceled':
                tb = traceback.format_exc()
            sentry_client.captureException()
        finally:
            if kwargs.get('private_data_dir', ''):
                try:
                    shutil.rmtree(kwargs['private_data_dir'], True)
                except OSError:
                    pass

            if kwargs.get('proot_temp_dir', ''):
                try:
                    shutil.rmtree(kwargs['proot_temp_dir'], True)
                except OSError:
                    pass

        self.post_run_hook(**kwargs)
        # instance.socketio_emit_status(instance.status)

        if status != 'successful' and not hasattr(settings, 'CELERY_UNIT_TEST'):
            if status == 'canceled':
                logger.warning('Task[%s] was canceled (rc=%s)' % (str(self.name), str(rc)))
            else:
                logger.warning('Task[%s] encountered an error (rc=%s), (tb=%s)' % (
                    str(self.name), str(rc), str(tb)))

        elif not hasattr(settings, 'CELERY_UNIT_TEST'):
            self.signal_finished()
