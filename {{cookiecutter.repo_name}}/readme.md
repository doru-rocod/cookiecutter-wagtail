{{ cookiecutter.project_name }}
==================

Mocht je willen draaien met Postgres, dan moet dat in je PATH zitten, bv.

    PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/ bin/pip install -r requirements.txt

Virtualenv
==============

    virtualenv .
    ./bin/pip install -r requirements/dev.txt

Initialiseren
=============

    ./bin/python manage.py migrate
    ./bin/python manage.py createsuperuser

Starten
=======
    ./bin/python manage.py runserver
