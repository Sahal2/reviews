# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-28 00:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0002_reviews_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
