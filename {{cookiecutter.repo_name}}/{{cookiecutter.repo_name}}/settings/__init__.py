import os

if not 'production' in os.environ['DJANGO_SETTINGS_MODULE']:
    from .dev import *
