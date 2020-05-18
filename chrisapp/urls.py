# URL dispatcher mapps URLs to python functions in views.py
from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("<int:joke_id>/", views.detail, name="detail"),
    path("add/", views.add, name="add"),
    path("email/<int:joke_id>/", views.email, name="email"),
    path("health/", views.health, name="health"),
]
