# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_sites', '0005_auto_20180331_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodproduct',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
