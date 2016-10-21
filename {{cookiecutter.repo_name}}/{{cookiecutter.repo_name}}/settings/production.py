# -*- coding: utf-8 -*-
import os
import dj_database_url

from .base import *

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

# Use Redis as the cache backend for extra performance

REDIS_IP = '192.168.165.192'
REDIS_PORT = '6379'
REDIS_LOCATION = '%s:%s' % (REDIS_IP, REDIS_PORT)
BROKER_URL = 'redis://%s' % REDIS_IP

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis:%s" % REDIS_LOCATION,
        'KEY_PREFIX': '{{ cookiecutter.repo_name }}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Compress static files offline and minify CSS
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

RAVEN_CONFIG = {
    # 'dsn': 'https://<key>:<secret>@sentry.fourdigits.nl/<project>',
}

# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()

# On Torchbox servers, many environment variables are prefixed with "CFG_"
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        env[key[4:]] = value


# Basic configuration

APP_NAME = env.get('APP_NAME', '{{ cookiecutter.repo_name }}')

if 'SECRET_KEY' in env:
    SECRET_KEY = env['SECRET_KEY']
else:
    SECRET_KEY = 'TO_BE_CHANGED_BY_POST_GEN_HOOK'

ALLOWED_HOSTS = [
    '.fourdigits.nl',  # Allow domain and subdomains
    '.fourdigits.nl.',  # Also allow FQDN and subdomains
]

if 'PRIMARY_HOST' in env:
    BASE_URL = 'http://%s/' % env['PRIMARY_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']

if 'CACHE_PURGE_URL' in env:
    INSTALLED_APPS += ( 'wagtail.contrib.wagtailfrontendcache', )
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.wagtailfrontendcache.backends.HTTPBackend',
            'LOCATION': env['CACHE_PURGE_URL'],
        },
    }

if 'STATIC_URL' in env:
    STATIC_URL = env['STATIC_URL']

if 'STATIC_DIR' in env:
    STATIC_ROOT = env['STATIC_DIR']

if 'MEDIA_URL' in env:
    MEDIA_URL = env['MEDIA_URL']

if 'MEDIA_DIR' in env:
    MEDIA_ROOT = env['MEDIA_DIR']


# Database

env.get('PGDATABASE', APP_NAME),
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.get('PGDATABASE', APP_NAME),
        'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
        'USER': env.get('PGDATABASE', APP_NAME),
        'HOST': '192.168.165.192',
        'PASSWD': '',
        # User, host and port can be configured by the PGUSER, PGHOST and
        # PGPORT environment variables (these get picked up by libpq).
        }
    }


# Elasticsearch

# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
#         'INDEX': '{{ cookiecutter.repo_name }}',
#         'ATOMIC_REBUILD': True,
#     },
# }

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'formatters': {
        'default': {
            'verbose': '[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s'
        }
    },
    'loggers': {
        '{{ cookiecutter.repo_name }}': {
            'handlers':     [],
            'level':        'INFO',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'wagtail': {
            'handlers':     [],
            'level':        'INFO',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.request': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.security': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
    },
}


if 'LOG_DIR' in env:
    # {{ cookiecutter.project_name }} log
    LOGGING['handlers']['{{ cookiecutter.repo_name }}_file'] = {
        'level':        'INFO',
        'class':        'cloghandler.ConcurrentRotatingFileHandler',
        'filename':     os.path.join(env['LOG_DIR'], '{{ cookiecutter.repo_name }}.log'),
        'maxBytes':     5242880, # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['wagtail']['handlers'].append('{{ cookiecutter.repo_name }}_file')

    # Wagtail log
    LOGGING['handlers']['wagtail_file'] = {
        'level':        'INFO',
        'class':        'cloghandler.ConcurrentRotatingFileHandler',
        'filename':     os.path.join(env['LOG_DIR'], 'wagtail.log'),
        'maxBytes':     5242880, # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['wagtail']['handlers'].append('wagtail_file')

    # Error log
    LOGGING['handlers']['errors_file'] = {
        'level':        'ERROR',
        'class':        'cloghandler.ConcurrentRotatingFileHandler',
        'filename':     os.path.join(env['LOG_DIR'], 'error.log'),
        'maxBytes':     5242880, # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['django.request']['handlers'].append('errors_file')
    LOGGING['loggers']['django.security']['handlers'].append('errors_file')


try:
    from .local import *
except ImportError:
    pass
