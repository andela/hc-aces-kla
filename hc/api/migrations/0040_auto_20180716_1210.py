# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-16 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180703_0928'),
        ('api', '0039_task_taskschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(
                max_length=100),
        ),
        migrations.RemoveField(
            model_name='task',
            name='profile',
        ),
        migrations.AddField(
            model_name='task',
            name='profile',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='accounts.Profile'),
        ),
        migrations.AlterField(
            model_name='taskschedule',
            name='task',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='api.Task'),
        ),
    ]
