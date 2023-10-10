"""
This module contains all database models for django.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy


class Visibility(models.TextChoices):
    """
    This 'enum' provides values for visibility settings.
    """

    moderator = "moderator", gettext_lazy("moderator")
    "Visible only to moderators"
    private = "private", gettext_lazy("private")
    "Visible only to author(s) and above"
    review = "review", gettext_lazy("review")
    "Visible only to reviewers and above"
    follower = "follower", gettext_lazy("follower")
    "Visible only to followers and above"
    user = "user", gettext_lazy("user")
    "Visible only to registered users"
    public = "public", gettext_lazy("public")
    "Visible to everyone"


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

    text = models.CharField(max_length=32, unique=True)


class Category(models.Model):
    """
    This model provides values for categories.
    """

    text = models.CharField(max_length=16, unique=True)

    # PHYSICS = "PHY", gettext_lazy("Physics")
    # BIOLOGY = "BIO", gettext_lazy("Biology")
    # CHEMISTRY = "CHE", gettext_lazy("Chemistry")
    # INFORMATICS = "INF", gettext_lazy("Informatics")
    # MATHS = "MAT", gettext_lazy("Mathematics")


class User(Followable, Commentable):
    """
    This class is only a dummy class yet. Instead, we should use or extend the user model of django's user management
    system if possible.
    """

    alias = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    follows = models.ManyToManyField(Followable, related_name="followed_by")
    likes = models.ManyToManyField(Commentable, related_name="liked_by")


class Comment(Commentable, Versionable):
    """
    This entity models a single comment. A comment relates to a commentable entity and a user.
    """

    content = models.TextField()
    commented_on = models.ForeignKey(Commentable, on_delete=models.RESTRICT, related_name="comments")
    written_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="written_comments")


class Project(Commentable, Followable):
    """
    This entity models a project. A project consists of one or more articles.
    """

    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128, null=True)
    description = models.TextField()
    thumbnail = models.ImageField()
    authors = models.ManyToManyField(User, related_name="projects")
    tags = models.ManyToManyField(Tag, related_name="projects")
    categories = models.ManyToManyField(Category, related_name="projects")
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.private)


class Article(Commentable, Versionable):
    """
    This entity models an article. An article relates to a project and one or more users.
    """

    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128, null=True)
    content = models.TextField()
    thumbnail = models.ImageField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="articles")
    authors = models.ManyToManyField(User, related_name="articles")
    tags = models.ManyToManyField(Tag, related_name="articles")
    categories = models.ManyToManyField(Category, related_name="articles")
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.private)
