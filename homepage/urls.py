"""
Include all routings of the homepage app
"""
from django.urls import path

from . import views

APP_NAME = "homepage"
urlpatterns = [
    path("", views.index, name="index"),
]
