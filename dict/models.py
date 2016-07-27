from django.db import models
from django.contrib.auth.models import User


class Text(models.Model):

    title = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    author = models.ForeignKey(User)
    audio = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.title


class Solution(models.Model):

    text = models.ForeignKey(Text)
    user_text = models.TextField()
    author = models.ForeignKey(User)


