"""
Include the views of the homepage app.
"""
# pylint: disable=unused-import
from django.shortcuts import render
from django.views.generic import TemplateView

from homepage.models import Categories


def index(request):
    """
    The index page of the homepage. It uses the `index.html` in the template folder.
    """

    template_name = "homepage/index.html"
    context = {"categories": Categories.choices}
    return render(request, template_name, context)
