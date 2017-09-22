# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-15 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0021_auto_20170915_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='fill_answer',
            name='answer2',
            field=models.CharField(default='', max_length=200, verbose_name='正确答案2'),
        ),
        migrations.AddField(
            model_name='fill_answer',
            name='answer3',
            field=models.CharField(default='', max_length=200, verbose_name='正确答案3'),
        ),
        migrations.AddField(
            model_name='fill_answer',
            name='answer4',
            field=models.CharField(default='', max_length=200, verbose_name='正确答案3'),
        ),
        migrations.AddField(
            model_name='fill_answer',
            name='answer5',
            field=models.CharField(default='', max_length=200, verbose_name='正确答案3'),
        ),
        migrations.AddField(
            model_name='fill_answer',
            name='is_only',
            field=models.BooleanField(default=False, verbose_name='答案唯一'),
        ),
    ]