# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 19:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('POC', '0002_auto_20160629_0312'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.RemoveField(
            model_name='loginuser',
            name='role',
        ),
    ]
