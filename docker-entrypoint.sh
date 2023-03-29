#!/bin/sh

python3 manage.py migrate
# python3 HikEMM_BE/setup_database.py
#python3 manage.py collectstatic --noinput
python3 manage.py runserver 0.0.0.0:8000
#nginx -g 'daemon off;'