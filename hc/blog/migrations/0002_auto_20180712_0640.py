# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-12 06:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish',)},
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=250, unique_for_date=b'publish'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[(b'draft', b'Draft'), (b'published', b'Published')], default=b'draft', max_length=10),
        ),
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
