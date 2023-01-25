"""
Includes all unit and integration tests for the homepage app.
"""
import re

# pylint: disable=unused-import
from django.test import TestCase, tag
from django.urls import reverse
from django.utils.translation import gettext_lazy


# Create your tests here.
@tag("page-index")
class TestIndexPage(TestCase):
    """
    Including all tests for the index page.
    """

    @tag("template")
    def test_template_used(self) -> None:
        """
        Test if the index view uses the correct template file
        """
        response = self.client.get(reverse("homepage:index"))
        self.assertTemplateUsed(response, "homepage/index.html")

    @tag("context")
    def test_categories(self) -> None:
        """
        Test if the categories are present and ok in views context.
        """
        response = self.client.get(reverse("homepage:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Physics")
        self.assertIn("categories", response.context)
        has_physics = False
        for category in response.context["categories"]:
            self.assertIn("label", category)
            if category["label"] == gettext_lazy("Physics"):
                has_physics = True
                break
        self.assert_(has_physics)

    @tag("routing")
    def test_category_subrouting(self) -> None:
        """
        Test if the category subrouting responses.
        """
        response = self.client.get(reverse("homepage:index", kwargs={"active_category": "physics"}))
        self.assertEqual(response.status_code, 200)

    @tag("html")
    def test_category_subrouting_HTML(self) -> None:
        """
        Test if the category subrouting works properly aka returns proper HTML.
        """
        response = self.client.get(reverse("homepage:index", kwargs={"active_category": "physics"}))
        self.assertEqual(response.status_code, 200)
        find_physics = (
            f'<a class="topic-link active" href="'
            f'{reverse("homepage:index", kwargs={"active_category": "physics"})}">Physics</a>'
        )
        self.assertContains(response, find_physics, html=True)
