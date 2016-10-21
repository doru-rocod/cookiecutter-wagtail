# -*- coding: utf-8 -*-
from .base import *

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