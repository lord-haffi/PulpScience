"""
This module contains all database models for django.
"""
from typing import TypeVar

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy


class Visibility(models.TextChoices):
    """
    This 'enum' provides values for visibility settings.
    """

    MODERATOR = "moderator", gettext_lazy("moderator")
    "Visible only to moderators"
    PRIVATE = "private", gettext_lazy("private")
    "Visible only to author(s) and above"
    REVIEW = "review", gettext_lazy("review")
    "Visible only to reviewers and above"
    FOLLOWER = "follower", gettext_lazy("follower")
    "Visible only to followers and above"
    USER = "user", gettext_lazy("user")
    "Visible only to registered users"
    PUBLIC = "public", gettext_lazy("public")
    "Visible to everyone"


T = TypeVar("T", bound="Versionable")


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
        if not self.versionable_id:  # pylint: disable=no-member
            self.created = timezone.now()
        if not self.version_group:
            max_version_group = Versionable.objects.aggregate(models.Max("version_group"))["version_group__max"]
            self.version_group = max_version_group + 1 if max_version_group is not None else 1
        if not self.version_number:
            self.version_number = 1
        # self.modified = timezone.now()
        return super().save(*args, **kwargs)

    def new_version(self: T) -> T:
        """
        Creates a new version of this entity. Copies all fields except the IDs and increments the
        'version_number'.
        """
        fields = {
            field.name: getattr(self, field.name)
            for field in self._meta.fields
            if field.name
            not in (
                "versionable_id",
                "versionable_ptr",
                "commentable_id",
                "commentable_ptr",
                "followable_id",
                "followable_ptr",
                "id",
            )
        }
        fields["version_number"] += 1
        return self.__class__(**fields)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["version_group", "version_number"], name="unique_version")]


class Commentable(models.Model):
    """
    This serves as super class to all entities being considered as 'commentable'.
    """

    commentable_id = models.BigAutoField(primary_key=True)


class Followable(models.Model):
    """
    This serves as super class to all entities being considered as 'followable'.
    """

    followable_id = models.BigAutoField(primary_key=True)


class Tag(models.Model):
    """
    This entity models a single tag. These tags can be used to categorize articles and projects.
    """

    name = models.CharField(max_length=32, unique=True)


class Category(models.Model):
    """
    This model provides values for categories.
    """

    name = models.CharField(max_length=16, unique=True)


class User(Followable, Commentable):
    """
    This class is only a dummy class yet. Instead, we should use or extend the user model of django's user management
    system if possible.
    """

    id = models.BigAutoField(primary_key=True)
    alias = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    follows = models.ManyToManyField(Followable, blank=True, related_name="followed_by")
    likes = models.ManyToManyField(Commentable, blank=True, related_name="liked_by")


class Comment(Commentable, Versionable):
    """
    This entity models a single comment. A comment relates to a commentable entity and a user.
    """

    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    commented_on = models.ForeignKey(Commentable, on_delete=models.RESTRICT, related_name="comments")
    written_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="written_comments")


class Project(Commentable, Followable):
    """
    This entity models a project. A project consists of one or more articles.
    """

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128, null=True)
    description = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    related_authors = models.ManyToManyField(User, blank=True, related_name="related_projects")
    related_tags = models.ManyToManyField(Tag, blank=True, related_name="related_projects")
    related_categories = models.ManyToManyField(Category, blank=True, related_name="related_projects")
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.PRIVATE)


class Article(Commentable, Versionable):
    """
    This entity models an article. An article relates to a project and one or more users.
    """

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128, null=True)
    content = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    related_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="related_articles")
    related_authors = models.ManyToManyField(User, blank=True, related_name="related_articles")
    related_tags = models.ManyToManyField(Tag, blank=True, related_name="related_articles")
    related_categories = models.ManyToManyField(Category, blank=True, related_name="related_articles")
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.PRIVATE)
