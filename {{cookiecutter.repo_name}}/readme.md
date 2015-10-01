{{ cookiecutter.project_name }}
==================
    
    PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/ bin/pip install -r requirements.txt

Virtualenv
==============

    virtualenv .
    ./bin/pip install -r requirements.txt

Starten
=======

    ./bin/python manage.py migrate
    ./bin/python manage.py createsuperuser
    ./bin/python manage.py runserver
