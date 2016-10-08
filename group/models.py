from django.db import models
from django.contrib.auth.models import Group, Permission, User
from django.conf import settings
from django.template.defaultfilters import slugify
from unidecode import unidecode
import random
import string


class GroupExt(Group):

    description = models.TextField(max_length=255, verbose_name='Опис')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    avatar = models.ImageField(blank=True, verbose_name=u'Аватар')

    class Meta:
        verbose_name = u'Група'
        verbose_name_plural = u'Групи'
        permissions = (
            ('group_member', 'Group member'),
            ('group_admin', 'Group admin'),
        )


class Invite(models.Model):

    group = models.ForeignKey(GroupExt)
    to_user = models.ForeignKey(User, verbose_name='Логін')
    token = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.token = ''.join(random.choice(string.ascii_uppercase +
                                           string.ascii_lowercase + string.digits) for x in range(6))
        super(Invite, self).save(*args, **kwargs)

    def __str__(self):
        return '{} -> {}'.format(self.group.name, self.to_user.username)


class Discussion(models.Model):

    title = models.CharField(max_length=255)
    text = models.TextField(max_length=800)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    group = models.ForeignKey(GroupExt)
    pubdate = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.slug = slugify(unidecode(self.title.lower()))
        super(Discussion, self).save(*args, **kwargs)

