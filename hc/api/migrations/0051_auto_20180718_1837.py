# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-18 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_merge_20180716_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='twilio_number',
            field=models.TextField(blank=True,
                                   default='+00000000000',
                                   null=True),
        ),
    ]
