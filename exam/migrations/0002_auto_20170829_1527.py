# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 07:27
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='single_q',
            name='caption',
            field=models.CharField(max_length=200, verbose_name='题目简化版'),
        ),
        migrations.AlterField(
            model_name='single_q',
            name='title',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='题目'),
        ),
    ]