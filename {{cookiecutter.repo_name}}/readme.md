{{ cookiecutter.project_name }}
==================

PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin/ bin/pip install -r requirements.txt

Virtualenv
==============
virtualenv .
./bin/pip install -r requirements.txt

Starten
=======
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
