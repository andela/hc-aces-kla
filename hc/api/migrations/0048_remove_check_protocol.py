# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-11 18:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20180710_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='protocol',
        ),
        migrations.RenameField(
            model_name='check',
            old_name='n_nags',
            new_name='number_of_nags',
        ),
    ]
