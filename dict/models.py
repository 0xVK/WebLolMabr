from django.db import models
from django.contrib.auth.models import User


class Text(models.Model):

    title = models.CharField(max_length=255)
    text = models.TextField(max_length=5500)
    author = models.ForeignKey(User)
    audio = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексти'


class Solution(models.Model):

    text = models.ForeignKey(Text)
    user_text = models.TextField()
    author = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Розвязок'
        verbose_name_plural = 'Розвязки'


