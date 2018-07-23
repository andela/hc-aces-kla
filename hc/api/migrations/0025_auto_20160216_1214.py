# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20160203_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='kind',
            field=models.CharField(choices=[('email', 'Email'),
                                            ('webhook', 'Webhook'),
                                            ('hipchat', 'HipChat'),
                                            ('slack', 'Slack'),
                                            ('pd', 'PagerDuty'),
                                            ('po', 'Pushover'),
                                            ('victorops', 'VictorOps')],
                                   max_length=20),
        ),
    ]
