#!/usr/bin/bash
#start jokesite in podman or OCP
if [ -z $1 ] ; then
    PORT=8080
else  
    PORT=$1
fi

# create database 
FILE=/var/tmp/jokesiteDatabaseCreated
if [ -f $FILE ]; then
    echo "Database already created"
else
    python3 "manage.py" "migrate"
    python3 "manage.py" "loaddata" "jokes.yaml"
    touch $FILE
fi
# Probs not needed, wass for podman + sqllite 
if [ -z ${DATABASE_SERVICE_NAME} ] ; then
    export DJANGO_SETTINGS_MODULE=jokesite.devsettings
    echo "Using development settings"
else
    export DJANGO_SETTINGS_MODULE=jokesite.settings
    echo "Using Postgres: ${DATABASE_SERVICE_NAME}"
fi

gunicorn jokesite.wsgi:application --bind 0.0.0.0:${PORT}