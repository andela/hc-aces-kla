# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-03 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_report_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='report_frequency',
            field=models.CharField(default=b'month', max_length=20),
        ),
    ]
