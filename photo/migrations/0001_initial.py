# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-22 04:53
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import photo.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='One Line Description')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', photo.fields.ThumbnailImageField(upload_to='photo/%Y/%m')),
                ('description', models.TextField(blank=True, verbose_name='Photo Description')),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name='Upload Date')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo.Album')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
