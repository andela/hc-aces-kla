# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-06 07:50
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20180706_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='protocol',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
