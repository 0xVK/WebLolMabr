# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-27 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0002_remove_solution_solved_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='user_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
