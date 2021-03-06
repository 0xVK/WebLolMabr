# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-22 05:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0007_invite_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupext',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars/group', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Логін'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='token',
            field=models.CharField(max_length=10),
        ),
    ]
