# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20171017_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='issueance',
            name='enrollment_no',
            field=models.IntegerField(default=16116076),
            preserve_default=False,
        ),
    ]
