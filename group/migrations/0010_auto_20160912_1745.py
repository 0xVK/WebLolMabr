# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-12 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_auto_20160825_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupext',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Аватар'),
        ),
    ]
