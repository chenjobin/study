# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_selections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selections',
            name='question',
        ),
        migrations.AddField(
            model_name='single_q',
            name='select_2',
            field=models.TextField(default='', max_length=200, verbose_name='选项2'),
        ),
        migrations.AddField(
            model_name='single_q',
            name='select_3',
            field=models.TextField(default='', max_length=200, verbose_name='选项3'),
        ),
        migrations.AddField(
            model_name='single_q',
            name='select_4',
            field=models.TextField(default='', max_length=200, verbose_name='选项4'),
        ),
        migrations.AddField(
            model_name='single_q',
            name='select_correct',
            field=models.CharField(default='', max_length=200, verbose_name='正确选项'),
        ),
        migrations.DeleteModel(
            name='Selections',
        ),
    ]