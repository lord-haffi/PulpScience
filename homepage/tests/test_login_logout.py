"""
Test the login and logout functionality.
"""
from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse


class TestLoginLogout(TestCase):
    """
    Includes tests to test the login and logout functionality.
    """

    @tag("page-login")
    def test_login_ability(self) -> None:
        """
        Test if you can log into in a general manner. It does not test the login page.
        """
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()

        self.assertTrue(self.client.login(username="testuser", password="12345"))

    @tag("page-login", "routing")
    def test_login_page_200(self) -> None:
        """
        Test if the login page is available
        """
        response = self.client.get(reverse("auth:login"))
        self.assertEqual(response.status_code, 200)

    @tag("page-login", "routing")
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

    @tag("page-logout", "routing")
    def test_logout_page_redirect(self) -> None:
        """
        Test if the logout page is available and redirects successfully
        """
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()

        self.assertTrue(self.client.login(username="testuser", password="12345"))
        response = self.client.get(reverse("auth:logout") + "?next=/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/index.html")
