# Generated by Django 4.1.5 on 2023-01-18 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Commentable",
            fields=[
                ("commentable_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("likes", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Followable",
            fields=[
                ("followable_id", models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Versionable",
            fields=[
                ("versionable_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("version_group", models.BigIntegerField()),
                ("version_number", models.PositiveIntegerField()),
                ("created", models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "followable_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="homepage.followable",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                ("following", models.ManyToManyField(related_name="followed_by", to="homepage.followable")),
            ],
            bases=("homepage.followable",),
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "followable_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        to="homepage.followable",
                    ),
                ),
                (
                    "commentable_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="homepage.commentable",
                    ),
                ),
                ("title", models.CharField(max_length=64)),
                ("subtitle", models.CharField(max_length=128, null=True)),
                ("description", models.TextField()),
                ("authors", models.ManyToManyField(related_name="authored_projects", to="homepage.user")),
            ],
            bases=("homepage.commentable", "homepage.followable"),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "commentable_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="homepage.commentable",
                    ),
                ),
                ("content", models.TextField()),
                (
                    "commented_on",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="comments",
                        to="homepage.commentable",
                    ),
                ),
                (
                    "commenter",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="homepage.user"),
                ),
            ],
            bases=("homepage.commentable",),
        ),
    ]