# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-17 17:23
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[(b'email', b'Email'), (b'webhook', b'Webhook'), (b'hipchat', b'HipChat'), (b'slack', b'Slack'), (b'pd', b'PagerDuty'), (b'po', b'Pushover'), (b'victorops', b'VictorOps'), (b'twiliosms', b'TwilioSms'), (b'twiliovoice', b'TwilioVoice')], max_length=20)),
                ('value', models.TextField(default=b'+256705357610', max_length=25)),
                ('email_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('tags', models.CharField(blank=True, max_length=500)),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('timeout', models.DurationField(default=datetime.timedelta(1))),
                ('grace', models.DurationField(default=datetime.timedelta(0, 3600))),
                ('n_pings', models.IntegerField(default=0)),
                ('last_ping', models.DateTimeField(blank=True, null=True)),
                ('alert_after', models.DateTimeField(blank=True, editable=False, null=True)),
                ('status', models.CharField(choices=[(b'up', b'Up'), (b'down', b'Down'), (b'new', b'New'), (b'paused', b'Paused')], default=b'new', max_length=6)),
                ('nag_intervals', models.DurationField(default=datetime.timedelta(1))),
                ('nag_after_time', models.DateTimeField(blank=True, null=True)),
                ('runs_too_often', models.BooleanField(default=False)),
                ('priority', models.IntegerField(default=1)),
                ('number_of_nags', models.IntegerField(default=0)),
                ('escalate', models.BooleanField(default=False)),
                ('twilio_number', models.TextField(blank=True, default=b'+00000000000', null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_status', models.CharField(max_length=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('error', models.CharField(blank=True, max_length=200)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Channel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Check')),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('scheme', models.CharField(default=b'http', max_length=10)),
                ('remote_addr', models.GenericIPAddressField(blank=True, null=True)),
                ('method', models.CharField(blank=True, max_length=10)),
                ('ua', models.CharField(blank=True, max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Check')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('task_type', models.CharField(choices=[(b'database_backups', b'database_backups'), (b'export_reports', b'export_reports')], max_length=100)),
                ('frequency', models.CharField(choices=[(b'daily', b'daily'), (b'weekly', b'weekly'), (b'monthly', b'monthly')], max_length=20)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
=======
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     verbose_name='ID',
                     serialize=False)),
                ('code',
                 models.UUIDField(
                     default=uuid.uuid4,
                     editable=False)),
                ('last_ping',
                 models.DateTimeField(
                     null=True,
                     blank=True)),
                ('user',
                 models.ForeignKey(
                     to=settings.AUTH_USER_MODEL)),
>>>>>>> [Feature #158174602] Finished code for saving tasks, applied pep8 standards
            ],
        ),
        migrations.CreateModel(
            name='TaskSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('send_email_updates', models.BooleanField(default=False)),
                ('next_run_date', models.DateTimeField(blank=True, null=True)),
                ('run_count', models.IntegerField(default=0)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Task')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='checks',
            field=models.ManyToManyField(to='api.Check'),
        ),
        migrations.AddField(
            model_name='channel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterIndexTogether(
            name='check',
            index_together=set([('status', 'user', 'alert_after', 'number_of_nags')]),
        ),
    ]
