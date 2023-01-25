from homepage.models import Category


class CategoryConverter:
    regex = "|".join([str(label).lower() for label in Category.labels])

    def to_python(self, value: str) -> Category:
        for member in Category:
            if member.label.lower() == value:
                return member
        raise ValueError(f"Unknown category {value}")

    def to_url(self, value: str) -> str:
        return value
