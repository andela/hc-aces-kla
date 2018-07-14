# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-12 06:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0048_remove_check_protocol'),
    ]

    operations = [

        migrations.AlterIndexTogether(
            name='check',
            index_together=set([('status', 'user', 'alert_after',
                                 'number_of_nags')]),
        ),
    ]