# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-28 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0003_solution_user_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='text',
            field=models.TextField(max_length=5500),
        ),
    ]
