# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0036_auto_20171012_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlewronganswer',
            name='is_show',
            field=models.BooleanField(default=True, verbose_name='显示'),
        ),
    ]
