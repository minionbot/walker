# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

import json
import os
import pipes
import re
import shutil
import time
import traceback
import uuid

try:
    import psutil
except:
    psutil = None

import pexpect
import retrying

from django.db import transaction, DatabaseError, OperationalError, close_old_connections
from django.conf import settings

from celery import Task
from celery.utils.log import get_logger

from raven.contrib.django.raven_compat.models import client

logger = get_logger('celery')

OPENSSH_KEY_ERROR = u"It looks like you're trying to use a private key " \
                    u"in OpenSSH format, which isn't supported by the installed version of " \
                    u"OpenSSH on this Tower instance. Try upgrading OpenSSH or providing" \
                    u" your private key in an different format. "
HIDDEN_PASSWORD = '**********'

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
    model = None
    abstract = True

    @retrying.retry(retry_on_exception = retry_if_database_error,
                    wait_fixed = 1000,
                    stop_max_attempt_number = 10)
    def update_model(self, pk, **updates):
        """
        Reload the model instance from the database and update the
        given fields.
        """
        with transaction.atomic():
            model = self.model.objects

            instance = model.get(pk=pk)
            if updates:
                update_fields = []
                for field, value in updates.items():

                    setattr(instance, field, value)
                    update_fields.append(field)

                instance.save(update_fields=update_fields)
            return instance

    def signal_finished(self, pk):
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

    def prepare_task_env(self, instance):
        for key, value in settings.AWX_TASK_ENV.items():
            if key == 'PATH':
                os.environ['PATH'] = os.environ.get('PATH', '/usr/bin') + ':' + value

    def build_env(self, instance, **kwargs):
        """
        Build environment dictionary for ansible-playbook.
        """
        env = dict(os.environ.items())

        for attr in dir(settings):
            if attr == attr.upper() and attr.startswith('ANSIBLE_'):
                env[attr] = str(getattr(settings, attr))

        for key, value in settings.AWX_TASK_ENV.items():
            env[key] = str(value)
            if key == 'PATH':
                env['PATH'] = os.environ.get('PATH', '/usr/bin') + ':' + value
                os.environ['PATH'] = env['PATH']

        python_paths = env.get('PYTHONPATH', '').split(os.pathsep)
        local_site_packages = self.get_path_to('..', 'lib', 'site-packages')
        if local_site_packages not in python_paths:
            python_paths.insert(0, local_site_packages)
        env['PYTHONPATH'] = os.pathsep.join(python_paths)
        if self.should_use_proot:
            env['PROOT_TMP_DIR'] = settings.AWX_PROOT_BASE_PATH

        env['JOB_STDOUT_FILENAME'] = '%d-%s.out' % (instance.pk, str(uuid.uuid1()))

        plugin_dir = self.get_path_to('..', 'plugins', 'callback')
        plugin_dirs = [plugin_dir]
        if hasattr(settings, 'AWX_ANSIBLE_CALLBACK_PLUGINS') and settings.AWX_ANSIBLE_CALLBACK_PLUGINS:
            plugin_dirs.append(settings.AWX_ANSIBLE_CALLBACK_PLUGINS)
        plugin_path = ':'.join(plugin_dirs)

        env['ANSIBLE_CALLBACK_PLUGINS'] = plugin_path
        env['ANSIBLE_LOOKUP_PLUGINS'] = self.get_path_to('..', 'plugins', 'lookup')
        env['ANSIBLE_LIBRARY'] = self.get_path_to('..', 'plugins', 'library')

        # for common base
        env['TANGO_TASK'] = '1'
        if isinstance(instance, (Job, ProjectUpdate,)) and hasattr(instance, 'work_id') and instance.work_id:
            env['TANGO_WORK_ID'] = str(instance.work_id)

        if 'KRB5CCNAME' in env:
            del env['KRB5CCNAME']
        return env

    def build_safe_env(self, instance, **kwargs):
        """
        Build environment dictionary, hiding potentially sensitive information
        such as passwords or keys.
        """
        hidden_re = re.compile('API|TOKEN|KEY|SECRET|PASS', re.I)
        urlpass_re = re.compile('^.*?://.?:(.*?)@.*?$')
        env = self.build_env(instance, **kwargs)
        for k, v in env.items():
            if k in ('REST_API_URL', 'AWS_ACCESS_KEY', 'AWS_ACCESS_KEY_ID'):
                continue
            elif k.startswith('ANSIBLE_'):
                continue
            elif hidden_re.search(k):
                env[k] = HIDDEN_PASSWORD
            elif type(v) == str and urlpass_re.match(v):
                env[k] = urlpass_re.sub(HIDDEN_PASSWORD, v)

        return env

    def args2cmdline(self, *args):
        return ' '.join([ pipes.quote(a) for a in args ])

    def get_ssh_key_path(self, instance, **kwargs):
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

    def build_args(self, instance, **kwargs):
        raise NotImplementedError

    def build_safe_args(self, instance, **kwargs):
        return self.build_args(instance, **kwargs)

    def run_pexpect(self, instance, args, cwd, env, passwords, stdout_handle):
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

        expect_list = []
        expect_passwords = {}
        pexpect_timeout = getattr(settings, 'PEXPECT_TIMEOUT', 5)

        while child.isalive():
            result_id = child.expect(expect_list, timeout=pexpect_timeout)
            if result_id in expect_passwords:
                child.sendline(expect_passwords[result_id])
            if logfile_pos != logfile.tell():
                logfile_pos = logfile.tell()
                last_stdout_update = time.time()
            instance = self.update_model(instance.pk)

        if child.exitstatus == 0:
            return 'successful', child.exitstatus
        else:
            return 'failed', child.exitstatus

    def pre_run_hook(self, instance, **kwargs):
        """
        Hook for any steps to run before the job/task starts
        """
        self.prepare_task_env(instance)

    def post_run_hook(self, instance, **kwargs):
        """
        Hook for any steps to run after job/task is complete.
        """
        if instance.dependent_job is None:
            return

        if instance.status == 'successful':
            instance.dependent_job.signal_start(**kwargs)
        elif instance.ignore_error is True and (instance.status == 'error' or instance.status == 'failed'):
            # Job Can Ignore Errors
            instance.update_fields(status='error_skipped')
            instance.socketio_emit_status(instance.status)
            instance.dependent_job.signal_start(**kwargs)
        else:
            # logger.error('It Looks like a job [%s] entry a not support branch with status [%s] ' % (
            #    instance.id, instance.status))
            if not isinstance(instance, (Job, ProjectUpdate)) or not instance.work:
                return

            from awx.main.tasks.notify import notify_dingding
            flow = instance.work
            notify_dingding.delay(flow.id, 'failed', 'wangjing@bytedance.com',
                                  flow.scm_pull_request_change.change_url)

    def run(self, pk, **kwargs):
        """
        Run the job/task and capture its output.
        """
        status, rc, tb = ('error', None, '')
        try:
            args = self.build_args(**kwargs)
            safe_args = self.build_safe_args(**kwargs)
            cwd = self.build_cwd(**kwargs)
            env = self.build_env(**kwargs)
            safe_env = self.build_safe_env(**kwargs)

            instance = self.update_model(pk, job_args=json.dumps(safe_args), job_cwd=cwd, job_env=safe_env, result_stdout_file=stdout_filename)
            status, rc = self.run_pexpect(instance, args, cwd, env, kwargs['passwords'])
        except Exception:
            if status != 'canceled':
                tb = traceback.format_exc()
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

            try:
                stdout_handle.flush()
                os.fsync(stdout_handle.fileno())
                stdout_handle.close()
            except Exception:
                client.captureException()

        instance = self.update_model(pk, status=status, result_traceback=tb, output_replacements=output_replacements)

        self.post_run_hook(instance, **kwargs)
        instance.socketio_emit_status(instance.status)

        if status != 'successful' and not hasattr(settings, 'CELERY_UNIT_TEST'):
            if status == 'canceled':
                logger.warning('Task %s(pk:%s) was canceled (rc=%s)' % (str(self.model.__class__), str(pk), str(rc)))
            else:
                logger.warning('Task %s(pk:%s) encountered an error (rc=%s), (tb=%s)' % (
                    str(self.model.__class__), str(pk), str(rc), str(tb)))

        elif not hasattr(settings, 'CELERY_UNIT_TEST'):
            self.signal_finished(pk)


