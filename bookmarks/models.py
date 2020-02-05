from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
    url         = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    isPublic    = models.BooleanField(default=False)
    user        = models.ForeignKey(User, related_name='bookmarks', on_delete = models.CASCADE)
