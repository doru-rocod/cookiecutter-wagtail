import os
import dj_database_url

from .base import *

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

# Use Redis as the cache backend for extra performance

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis:192.168.165.192:6379',
        'KEY_PREFIX': '{{ cookiecutter.repo_name }}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

REDIS_LOCATION = '192.168.165.192:6379'
BROKER_URL = 'redis://192.168.165.192'

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
    SECRET_KEY = ''  # Put some random string here (>30 chars)

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


# Redis
# Redis location can either be passed through with REDIS_HOST or REDIS_SOCKET

if 'REDIS_URL' in env:
    REDIS_LOCATION = env['REDIS_URL']
    BROKER_URL = env['REDIS_URL']

elif 'REDIS_HOST' in env:
    REDIS_LOCATION = env['REDIS_HOST']
    BROKER_URL = 'redis://%s' % env['REDIS_HOST']

elif 'REDIS_SOCKET' in env:
    REDIS_LOCATION = 'unix://%s' % env['REDIS_SOCKET']
    BROKER_URL = 'redis+socket://%s' % env['REDIS_SOCKET']

else:
    REDIS_LOCATION = None


if REDIS_LOCATION is not None:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_LOCATION,
            'KEY_PREFIX': APP_NAME,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }


# Elasticsearch

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': '{{ cookiecutter.repo_name }}',
        'ATOMIC_REBUILD': True,
    },
}

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
