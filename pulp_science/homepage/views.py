"""
Include the views of the homepage app.
"""
# pylint: disable=unused-import
from django.shortcuts import render  # type:ignore[import]
from django.views.generic import TemplateView  # type:ignore[import]


class IndexView(TemplateView):
    """
    The index page of the homepage. It uses the `index.html` in the template folder.
    """

    template_name = "homepage/index.html"
