"""
Register your models here.
"""
# pylint: disable=unused-import
from django.contrib import admin

from homepage import models

# Register your models here.
admin.site.register(models.Followable)
admin.site.register(models.Commentable)
admin.site.register(models.Versionable)
admin.site.register(models.Comment)
admin.site.register(models.User)
admin.site.register(models.Project)
