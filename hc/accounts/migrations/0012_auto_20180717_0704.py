# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-17 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_merge_20180716_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='report_frequency',
            field=models.CharField(default='month', max_length=20),
        ),
    ]
