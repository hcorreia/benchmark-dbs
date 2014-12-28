#!/usr/bin/env python
import os
import sys

import conf


############
# Settings #
############

from django.conf import settings

DEBUG = conf.DJANGO_DEBUG
SECRET_KEY = os.environ.get('SECRET_KEY', 'ova%(9y1%_=3rtp35x7q#tj^nmc%(1*tfohu73i2xex@0hs8*4')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(),
    DATABASES={
        'default': {
            'ENGINE':   'django.db.backends.sqlite3',
            'NAME':     '/dev/shm/benchdb.db',
        },
        'mysql': {
            'ENGINE':   'django.db.backends.mysql',
            'NAME':     conf.mysql['db'],
            'USER':     conf.mysql['user'],
            'PASSWORD': conf.mysql['passwd'],
            'HOST':     conf.mysql['host'],
            'PORT':     conf.mysql['port'],
            # 'STORAGE_ENGINE': 'MYISAM',
            # 'OPTIONS': {
            #     'init_command': 'SET storage_engine=MYISAM',
            # },
        },
        'pg': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     conf.pg['database'],
            'USER':     conf.pg['user'],
            'PASSWORD': conf.pg['password'],
            'HOST':     conf.pg['host'],
            'PORT':     conf.pg['port'],
        },
        'sqlite3': {
            'ENGINE':   'django.db.backends.sqlite3',
            'NAME':     conf.sqlite3['file'],
        },
    },
    INSTALLED_APPS=('app',),
)


#########
# Views #
#########

from django.http import HttpResponse, JsonResponse

def index(request):
    return JsonResponse({'content': 'Hello World'})


########
# Urls #
########

from django.conf.urls import url

urlpatterns = (
    url(r'^$', index),
)


##################
# Execute / WSGI #
##################

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
else:
    from django.core.wsgi import get_wsgi_application
    application = app = get_wsgi_application()
