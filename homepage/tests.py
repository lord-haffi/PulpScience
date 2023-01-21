"""
Includes all unit and integration tests for the homepage app.
"""
# pylint: disable=unused-import
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy


# Create your tests here.
class TestIndexPage(TestCase):
    def test_template_used(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertTemplateUsed(response, "homepage/index.html")

    def test_categories(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Physics")
        self.assertIn("categories", response.context)
        self.assertIn(("PHY", gettext_lazy("Physics")), response.context["categories"])
