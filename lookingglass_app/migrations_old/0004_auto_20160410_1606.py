# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 20:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lookingglass_app', '0003_auto_20160410_1253'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='Images',
        ),
    ]
