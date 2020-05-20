FROM registry.access.redhat.com/ubi8/python-36 
LABEL version="0.2" \
      description="A Simple Django Joke Application" \
      io.openshift.expose-services="8080:http"

USER root
RUN mkdir -p /opt/app-root/src && chown -R 1001:0 /opt/app-root/src && yum -y install bind-utils
USER 1001 
WORKDIR /opt/app-root/src
COPY requirements.txt ./
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

ADD . ./

ENV PORT 8080
EXPOSE 8080

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL='' python manage.py collectstatic --noinput

CMD [ "/opt/app-root/src/start-application.sh", "8080" ]
