# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20170815_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='read_num',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
