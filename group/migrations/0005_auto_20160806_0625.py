# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-06 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_discussion'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='pubdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
