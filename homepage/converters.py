"""
Contains custom converters to convert custom types in URL parameters.
"""
from homepage.models import Category


class CategoryConverter:
    """
    Converter for Enum `Category`.
    """

    regex = "|".join([str(label).lower() for label in Category.labels])

    def to_python(self, value: str) -> Category:
        """
        Converts provided parameter to Category enum instance.
        :param value: Provided URL parameter as string
        :return: The corresponding `Category` enum object
        """
        for member in Category:
            if member.label.lower() == value:
                return member
        raise ValueError(f"Unknown category {value}")

    def to_url(self, value: str) -> str:
        """
        Converts provided category to a string to use it inside URLs.
        :param value: The category instance (as string? Idk why)
        :return: The string representation for the URL
        """
        return value
