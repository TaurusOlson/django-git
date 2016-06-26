# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 10:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('sha', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('commit_time', models.DateTimeField()),
                ('author', models.CharField(max_length=30)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('first_time', models.DateTimeField()),
                ('last_time', models.DateTimeField()),
                ('commits_count', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='commit',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='git.Project'),
        ),
    ]