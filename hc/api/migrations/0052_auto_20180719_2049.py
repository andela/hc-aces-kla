# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-19 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_profile_ping_log_limit'),
        ('api', '0051_merge_20180716_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('date_run', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('task_type', models.CharField(
                    choices=[
                        (b'database_backups', b'database_backups'),
                        (b'export_reports', b'export_reports')],
                    max_length=100)),
                ('frequency', models.CharField(
                    choices=[(b'daily', b'daily'),
                             (b'weekly', b'weekly'),
                             (b'monthly', b'monthly')],
                    max_length=20)),
                ('profile', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('send_email_updates', models.BooleanField(default=False)),
                ('next_run_date', models.DateTimeField(blank=True, null=True)),
                ('run_count', models.IntegerField(default=0)),
                ('task', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='api.Task')),
            ],
        ),
        migrations.AddField(
            model_name='backup',
            name='schedule',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='api.TaskSchedule'),
        ),
        migrations.AddField(
            model_name='backup',
            name='task',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='api.Task'),
        ),
    ]