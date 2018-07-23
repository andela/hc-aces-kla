# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-28 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='twilio_number',
            field=models.TextField(default="+256705357610"),
        ),
        migrations.AlterField(
            model_name='channel',
            name='kind',
            field=models.CharField(choices=[('email', 'Email'),
                                            ('webhook', 'Webhook'),
                                            ('hipchat', 'HipChat'),
                                            ('slack', 'Slack'),
                                            ('pd', 'PagerDuty'),
                                            ('po', 'Pushover'),
                                            ('victorops', 'VictorOps'),
                                            ('twilio', 'Twilio')],
                                   max_length=20),
        ),
    ]