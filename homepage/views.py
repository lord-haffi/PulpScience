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
    for category in Category.objects.all():
        add_class = "" if active_category is None or active_category != category else " active"
        categories.append(
            {
                "label": category.name.capitalize(),
                "add_class": add_class,
                "link": reverse("homepage:index", kwargs={"active_category": category.name}),
            }
        )
    page_title = "Pulp Science"
    if active_category is not None:
        page_title += f" - {active_category.name.capitalize()}"

    template_name = "homepage/index.html"
    current_url = (
        reverse("homepage:index")
        if active_category is None
        else reverse("homepage:index", kwargs={"active_category": active_category.name})
    )
    if request.user.is_authenticated:
        loginout = "Logout"
        loginout_url = reverse("auth:logout") + f"?next={current_url}"
    else:
        loginout = "Login"
        loginout_url = reverse("auth:login") + f"?next={current_url}"
    context = {
        "categories": categories,
        "page_title": page_title,
        "loginout": loginout,
        "loginout_url": loginout_url,
        "current_url": current_url,
    }
    return render(request, template_name, context)
