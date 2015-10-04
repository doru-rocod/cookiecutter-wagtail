from .base import *

INSTALLED_APPS += ['debug_toolbar', ]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGEME!!!'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Process all tasks synchronously.
# Helpful for local development and running tests
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True

INSTALLED_APPS = ['django_nose'] + INSTALLED_APPS
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--with-xcoverage',
    '--cover-package=ecommerce',
    '--cover-erase',
    '--nocapture',
    '--with-doctest',
    '--ignore-files=^[0-9]{4}.*',
    '--ignore-files=^fabfile',
    '--ignore-files=^setup',
    '--ignore-files=^meta.py',
    '--ignore-files=config.py',
    '--ignore-files=acc.py',
    '--ignore-files=dev.py',
    '--ignore-files=prd.py',
    '--ignore-files=tst.py',
    '--verbosity=2',
    '--exe',
    ]

try:
    from .local import *
except ImportError:
    pass
