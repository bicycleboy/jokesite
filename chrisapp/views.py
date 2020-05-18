# Each view processes a web request and returns web response (actually the controller in MVC pattern, View is the HTML templates)

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.db import connections
from django.db.utils import OperationalError

import logging
import sys
from .forms import JokeForm, EmailForm
from .models import Joke

# Home page, list all jokes
def index(request):

    db_conn = connections["default"]
    try:
        c = db_conn.cursor()
    except OperationalError:
        messages.success(request, "Waiting for the database...")
        joke_list = 0
    else:
        joke_list = Joke.objects.order_by("-joke_text")[:50]

    context = {"joke_list": joke_list}

    return render(request, "chrisapp/index.html", context)


# Show Punchline
def detail(request, joke_id):
    joke = get_object_or_404(Joke, pk=joke_id)
    return render(request, "chrisapp/detail.html", {"joke": joke})


# Add a new joke
def add(request):
    if request.method == "POST":

        # create a form instance and populate it with data from the request:
        form = JokeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            #
            form.save()
            messages.success(request, "Thanks for your joke!")
            # redirect to main:
            return HttpResponseRedirect("/chrisapp/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = JokeForm()

    return render(request, "chrisapp/add.html", {"form": form})


# Email a joke to the user
def email(request, joke_id):
    joke = get_object_or_404(Joke, pk=joke_id)
    if request.method == "POST":

        # create a form instance and populate it with data from the request:

        form = EmailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            messages.success(request, "Your joke email is on the way!")
            # process the data in form.cleaned_data as required
            #
            host = request.get_host()
            to = form.cleaned_data["your_email"]
            # Todo: use templates not hardcode here https://docs.djangoproject.com/en/dev/ref/templates/api
            subject, from_email = (
                "Your new joke from Chris' rockin' joke app!",
                settings.DEFAULT_FROM_EMAIL,
            )
            text_content = joke.joke_text + " " + joke.punchline_text
            html_content = (
                "<p>"
                + joke.joke_text
                + "<br><strong>"
                + joke.punchline_text
                + "</strong><br><br>Get more top jokes at <a href=http://"
                + host
                + ">"
                + host
                + "</a></p>"
            )
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # redirect to main:

            return HttpResponseRedirect("/chrisapp/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmailForm()

    return render(request, "chrisapp/email.html", {"joke": joke})

# support for a health heartbeat 
def health(request):
    return HttpResponseRedirect("/chrisapp/")
