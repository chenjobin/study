# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20170829_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='single_q',
            name='select_correct',
            field=models.TextField(default='', max_length=200, verbose_name='正确选项'),
        ),
    ]