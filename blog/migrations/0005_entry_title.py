# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170813_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='title',
            field=models.CharField(default=1, max_length=256, verbose_name='标题'),
            preserve_default=False,
        ),
    ]
