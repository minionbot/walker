#!/usr/bin/env bash

WORK_DIR='/home/wangjing/opt/walker/'

cd ${WORK_DIR}
. .env/bin/activate
# .env/bin/uwsgi -x conf/uwsgi.xml --chdir=${WORK_DIR} --home=${WORK_DIR}/.env
python manage.py runserver_plus 0.0.0.0:9321 >log/uwsgi.log 2>&1