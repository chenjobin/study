# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-15 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0022_auto_20170915_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fill_answer',
            name='answer5',
        ),
        migrations.AlterField(
            model_name='fill_answer',
            name='is_only',
            field=models.BooleanField(default=False, verbose_name='答案形式确定'),
        ),
    ]