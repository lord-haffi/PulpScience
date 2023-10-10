"""
Contains custom converters to convert custom types in URL parameters.
"""
from django.db.utils import OperationalError

from homepage.models import Category


class CategoryConverter:
    """
    Converter for Model `Category`.
    """

    @property
    def regex(self) -> str:
        """
        Returns a regex string to match all categories.
        It is implemented as property because Django calls like `python manage.py migrate` will fail if the database
        has no table `homepage_category` yet. This is because this property is called during the migration process
        (idk why, some initialization process of Django I guess).
        """
        try:
            return "|".join([category.name for category in Category.objects.all()])
        except OperationalError as error:
            if "no such table" not in str(error):
                raise
            return ""

    def to_python(self, value: str) -> Category:
        """
        Converts provided parameter to Category enum instance.
        :param value: Provided URL parameter as string
        :return: The corresponding `Category` enum object
        """
        try:
            return Category.objects.get(name=value.lower())
        except Category.DoesNotExist as error:
            raise ValueError(f"Unknown category {value.lower()}") from error

    def to_url(self, value: str) -> str:
        """
        Converts provided category to a string to use it inside URLs.
        :param value: The category instance (as string? Idk why)
        :return: The string representation for the URL
        """
        return value
