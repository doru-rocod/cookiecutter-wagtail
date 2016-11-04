{{ cookiecutter.project_name }}
==================

Mocht je willen draaien met Postgres, dan moet dat in je PATH zitten, bv.

    PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/ bin/pip install -r requirements.txt

Maak vervolgens een database aan met:

    createdb {{ cookiecutter.repo_name }}

Virtualenv
==========

    virtualenv .
    ./bin/pip install -r requirements/dev.txt

Initialiseren
=============

    ./bin/python manage.py migrate
    ./bin/python manage.py createsuperuser

Starten
=======
    ./bin/python manage.py runserver

Development
===========

Whenever you make changes to models you need to create a migration to reflect this changes in the database. You can do
this with the `makemigrations` management command

    ./bin/python manage.py makemigrations <app_label>

This will try to create the necessary migrations for your updates. You can also run `makemigrations` without the app
label, the command will search through all the applications and see if it is necessary to create a migration.

Once the migrations are in place you need to migrate

    ./bin/python manage.py migrate

This will apply the migrations to the database.

If your ready developing your feature you could choose to squash all the migrations into one big one before making a
pull request.

    ./bin/python manage.py squashmigration


Deployment
==========

Update the production installation with::

    ./bin/fab -R production deploy


This will run on the first configured worker
All good? Then reload uwsgi::

    ./bin/fab -R production reload