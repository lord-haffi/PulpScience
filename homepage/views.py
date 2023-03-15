"""
Include the views of the homepage app.
"""
from typing import Optional

# pylint: disable=unused-import
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from homepage.models import Category


def index(request, active_category: Optional[Category] = None):
    """
    The index page of the homepage. It uses the `index.html` in the template folder.
    """
    categories = []
    for member in Category:
        add_class = "" if active_category is None or active_category != member else " active"
        categories.append(
            {
                "label": member.label,
                "add_class": add_class,
                "link": reverse("homepage:index", kwargs={"active_category": member.label.lower()}),
            }
        )
    page_title = "Pulp Science"
    if active_category is not None:
        page_title += f" - {active_category.label}"

    template_name = "homepage/index.html"
    context = {"categories": categories, "page_title": page_title}
    return render(request, template_name, context)
