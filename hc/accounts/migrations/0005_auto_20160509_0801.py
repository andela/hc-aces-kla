# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-09 08:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_profile_api_key'),
    ]

    operations = [
    ]
