# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-29 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20180629_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='value',
            field=models.TextField(default=256705357610, max_length=25),
        ),
    ]