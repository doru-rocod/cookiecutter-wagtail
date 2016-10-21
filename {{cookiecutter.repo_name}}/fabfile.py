# -*- coding: utf-8 -*-
"""Fabric scripts for easy deployment to staging / production."""
from fabric.api import *
from fabric.context_managers import cd

env.roledefs = {
    'production': [],
    'staging': [],
}

env.user = 'root'
env.use_ssh_config = True

@roles('production')
def deploy_production():
    """Deploy to production."""
    with cd('/django/{{ cookiecutter.repo_name }}'):
        run('git pull origin master')
        run('bin/pip install --update -r requirements/prd.txt')
        run('bin/python manage.py migrate --noinput --settings={{ cookiecutter.repo_name }}.settings.production')
        run('bin/python manage.py collectstatic --noinput --settings={{ cookiecutter.repo_name }}.settings.production')
        run('bin/python manage.py compress --settings={{ cookiecutter.repo_name }}.settings.production')
        run('bin/python manage.py update_index --settings={{ cookiecutter.repo_name }}.settings.production')

        run('service uwsgi restart')
        run('/etc/init.d/nginx reload')
