"""
Configuration for the homepage apps.
"""
from django.apps import AppConfig  # type:ignore[import]


class HomepageConfig(AppConfig):
    """
    Configuration for the homepage app.
    """

    name = "homepage"
    default_auto_field = "django.db.models.BigAutoField"
