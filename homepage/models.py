"""
This module contains all database models for django.
"""
from django.db import models  # type:ignore[import]
from django.utils import timezone  # type:ignore[import]
from django.utils.translation import gettext_lazy


class Categories(models.TextChoices):
    """
    This 'enum' provides values for categories.
    """

    PHYSICS = "PHY", gettext_lazy("Physics")
    BIOLOGY = "BIO", gettext_lazy("Biology")
    CHEMISTRY = "CHE", gettext_lazy("Chemistry")
    INFORMATICS = "INF", gettext_lazy("Informatics")
    MATHS = "MAT", gettext_lazy("Mathematics")


class Versionable(models.Model):
    """
    This serves as super class to all entities being considered as 'versionable'.
    An entity relate to a 'version_group' as its ID and the 'version_number' as its version.
    I.e. when a versionable entity gets updated a new entry with the same 'version_group' but a newer 'version_number'
    will be created.
    """

    versionable_id = models.BigAutoField(primary_key=True)
    version_group = models.BigIntegerField()
    version_number = models.PositiveIntegerField()
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """
        Automatically set creation date
        """
        if not self.id:  # pylint: disable=no-member
            self.created = timezone.now()
        # self.modified = timezone.now()
        return super().save(*args, **kwargs)


class Commentable(models.Model):
    """
    This serves as super class to all entities being considered as 'commentable'.
    """

    commentable_id = models.BigAutoField(primary_key=True)
    likes = models.PositiveIntegerField(default=0)


class Followable(models.Model):
    """
    This serves as super class to all entities being considered as 'followable'.
    """

    followable_id = models.BigAutoField(primary_key=True)


class User(Followable):
    """
    This class is only a dummy class yet. Instead, we should use or extend the user model of django's user management
    systen if possible.
    """

    name = models.CharField(max_length=32)
    following = models.ManyToManyField(Followable, related_name="followed_by")


class Comment(Commentable):
    """
    This entity models a single comment. A comment relates to a commentable entity and a user.
    """

    content = models.TextField()
    commented_on = models.ForeignKey(Commentable, on_delete=models.SET_NULL, null=True, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Project(Commentable, Followable):
    """
    This entity models a project. A project consists of one or more articles.
    """

    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128, null=True)
    description = models.TextField()
    authors = models.ManyToManyField(User, related_name="authored_projects")
