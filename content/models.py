# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from PIL import Image


class Article(models.Model):

    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    rating = models.IntegerField(default=0, verbose_name=u'Рейтинг')
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Стаття'
        verbose_name_plural = u'Статті'
        ordering = ('-pub_date', )


class Comment(models.Model):

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u'Коментарій'
        verbose_name_plural = u'Коментарії'
        ordering = ('-pub_date',)
