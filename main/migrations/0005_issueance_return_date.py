# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 08:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20171002_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='issueance',
            name='return_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]