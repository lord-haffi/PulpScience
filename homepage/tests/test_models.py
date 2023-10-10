"""
Test basic functionality of the models of the homepage app.
Note that the tests do not test that much (intentionally) to keep some flexibility.
"""

from django.test import TestCase, tag

from homepage import models


@tag("models")
class TestModels(TestCase):
    """
    Test basic functionality of the models of the homepage app.
    """

    def test_create_and_versioning_article(self) -> None:
        """
        Test if an article can be created and tests if the relations work.
        """
        user = models.User(alias="testuser", name="Test User")
        user.save()
        tag_foo = models.Tag(name="foo")
        tag_foo.save()
        tag_bar = models.Tag(name="bar")
        tag_bar.save()
        project = models.Project(
            title="Test Project",
            subtitle="Test Subtitle",
            description="Test Description",
        )
        project.save()
        project.refresh_from_db()
        project.related_authors.add(user)
        project.related_tags.add(tag_foo, tag_bar)
        project.related_categories.add(models.Category.objects.get(name="physics"))
        project.save()
        article = models.Article(
            title="Test Article",
            subtitle="Test Subtitle",
            content="Test Content",
            related_project=project,
        )
        article.save()
        article.refresh_from_db()
        article.related_authors.add(user)
        article.related_tags.add(tag_foo)
        article.related_categories.add(models.Category.objects.get(name="physics"))
        article.save()

        loaded_article: models.Article = models.Article.objects.get(title="Test Article")
        self.assertEqual(loaded_article.title, "Test Article")
        self.assertEqual(loaded_article.content, "Test Content")

        modified_article = loaded_article.new_version()
        modified_article.title = "Modified Test Article"
        modified_article.save()

        loaded_modified_article = models.Article.objects.get(
            version_group=loaded_article.version_group, version_number=2
        )
        self.assertEqual(loaded_modified_article.title, "Modified Test Article")
