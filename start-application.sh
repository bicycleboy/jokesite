#!/usr/bin/bash
#start jokesite in podman or OCP
if [ -z $1 ] ; then
    PORT=8080
else  
    PORT=$1
fi

# Probs not needed, was for podman + sqllite 
if [ -z ${DATABASE_SERVICE_NAME} ] ; then
    export DJANGO_SETTINGS_MODULE=jokesite.devsettings
    echo "start-application.sh: Using development settings"
else 
    # Could not get init container to work
    for i in {1..5}; do
        nslookup ${DATABASE_SERVICE_NAME} | grep "No answer"
        if [ $? -eq 1 ]; then
            echo "start-application.sh: Found DB service ${DATABASE_SERVICE_NAME}"
            break
        else
            echo "start-application.sh: Waiting for DB service..."
            sleep 2
        fi
    done
    echo "start-application.sh: Creating Database"
    python3 "manage.py" "migrate"
    echo "start-application.sh: Populating Database"
    python3 "manage.py" "loaddata" "jokes.yaml"
    export DJANGO_SETTINGS_MODULE=jokesite.settings
    echo "start-application.sh: Using Postgres DB: ${DATABASE_SERVICE_NAME}"
fi

gunicorn jokesite.wsgi:application --bind 0.0.0.0:${PORT}