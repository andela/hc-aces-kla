# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-16 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20180716_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskschedule',
            name='next_run_time',
        ),
    ]
