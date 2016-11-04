# -*- coding: utf-8 -*-
"""Fabric scripts for easy deployment to staging / production."""
from fabric.api import *
from fabric.context_managers import cd

env.roledefs = {
    'production': ['worker04.fourdigits.nl', 'worker05.fourdigits.nl'],
    'staging': [],
    'test': ['lightspeed.fourdigits.nl']
}

env.user = '{{ cookiecutter.repo_name }}'

env.always_use_pty = False
env.forward_agent = True
env.use_ssh_config = True
env.first_worker = env.roledefs['production'][0]


@hosts(env.first_worker)
def deploy_staging():
    """Deploy to staging environment."""
    with cd('/home/{{ cookiecutter.repo_name }}/application/{{ cookiecutter.repo_name }}'):
        run('git pull origin master')
        run('./bin/pip install -r requirements/prd.txt')
        run('bin/python manage.py migrate --noinput --settings={{ cookiecutter.repo_name }}.settings.production')
        run('bin/python manage.py collectstatic --noinput --settings={{ cookiecutter.repo_name }}.settings.production')
        run('bin/python manage.py compress --settings={{ cookiecutter.repo_name }}.settings.production')
        run('bin/python manage.py update_index --settings={{ cookiecutter.repo_name }}.settings.production')

def reload():
    with cd('/home/{{ cookiecutter.repo_name }}/'):
        run('touch uwsgi-reload')