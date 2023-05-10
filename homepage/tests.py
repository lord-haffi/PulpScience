"""
Includes all unit and integration tests for the homepage app.
"""
from django.contrib.auth.models import User

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
        self.assertTrue(has_physics)

    @tag("routing")
    def test_category_subrouting(self) -> None:
        """
        Test if the category subrouting responses.
        """
        response = self.client.get(reverse("homepage:index", kwargs={"active_category": "physics"}))
        self.assertEqual(response.status_code, 200)

    @tag("html")
    def test_category_subrouting_html(self) -> None:
        """
        Test if the category subrouting works properly aka returns proper HTML.
        """
        response = self.client.get(reverse("homepage:index", kwargs={"active_category": "physics"}))
        self.assertEqual(response.status_code, 200)
        find_physics = (
            f'<a class="topic-link active" data-url="'
            f'{reverse("homepage:index", kwargs={"active_category": "physics"})}">Physics</a>'
        )
        self.assertContains(response, find_physics, html=True)

    @tag("login")
    def test_login_ability(self) -> None:
        """
        Test if you can log into in a general manner. It does not test the login page.
        """
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()

        self.assertTrue(self.client.login(username="testuser", password="12345"))

    @tag("login", "routing")
    def test_login_page_200(self) -> None:
        """
        Test if the login page is available
        """
        response = self.client.get(reverse("auth:login"))
        self.assertEqual(response.status_code, 200)

    @tag("login", "routing")
    def test_login_page_redirect(self) -> None:
        """
        Test if the login page is available and redirects successfully
        """
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()

        response = self.client.post(
            reverse("auth:login") + "?next=/", {"username": "testuser", "password": "12345"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/index.html")

    @tag("logout", "routing")
    def test_logout_page_redirect(self) -> None:
        """
        Test if the logout page is available and redirects successfully
        """
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()

        self.assertTrue(self.client.login(username="testuser", password="12345"))
        response = self.client.get(reverse("auth:logout") + f"?next=/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/index.html")
