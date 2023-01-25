"""
Include all routings of the homepage app
"""
from django.urls import path, register_converter

from . import views
from .converters import CategoryConverter

APP_NAME = "homepage"

register_converter(CategoryConverter, "category")

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<category:active_category>", views.index, name="index"),
]
