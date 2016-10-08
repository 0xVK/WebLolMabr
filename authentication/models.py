from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(verbose_name=u'Фотографія')
    about = models.TextField(max_length=255)
    is_extend = models.BooleanField(default=False)
    status = models.CharField(max_length=25)

    class Meta:
        db_table = 'auth_profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)