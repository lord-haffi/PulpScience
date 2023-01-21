"""
Includes all unit and integration tests for the homepage app.
"""
# pylint: disable=unused-import
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class TestIndexPage(TestCase):
    def test_categories(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Physics")
        self.assertIn("categories", response.context)
        # self.assertQuerysetEqual(response.context['latest_question_list'], [])
