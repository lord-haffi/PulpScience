"""
Include all routings of the homepage app
"""
from django.urls import path  # type:ignore[import]

from . import views

APP_NAME = "homepage"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
