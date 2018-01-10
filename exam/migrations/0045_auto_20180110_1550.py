# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-10 07:50
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0044_auto_20180110_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fill_q',
            name='answer_detail',
            field=DjangoUeditor.models.UEditorField(blank=True, default='略', verbose_name='答案解析'),
        ),
        migrations.AlterField(
            model_name='single_q',
            name='title',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='题目'),
        ),
    ]
