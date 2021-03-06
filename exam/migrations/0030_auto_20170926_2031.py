# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0029_auto_20170926_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fillwronganswer',
            name='correct_times',
            field=models.PositiveIntegerField(default=0, verbose_name='第一次做对'),
        ),
        migrations.AlterField(
            model_name='fillwronganswer',
            name='first_right_times',
            field=models.PositiveIntegerField(default=0, verbose_name='答对次数'),
        ),
        migrations.AlterField(
            model_name='fillwronganswer',
            name='wrong_times',
            field=models.PositiveIntegerField(default=0, verbose_name='错误次数'),
        ),
        migrations.AlterField(
            model_name='singlewronganswer',
            name='correct_times',
            field=models.PositiveIntegerField(default=0, verbose_name='第一次做对'),
        ),
        migrations.AlterField(
            model_name='singlewronganswer',
            name='first_right_times',
            field=models.PositiveIntegerField(default=0, verbose_name='答对次数'),
        ),
        migrations.AlterField(
            model_name='singlewronganswer',
            name='wrong_times',
            field=models.PositiveIntegerField(default=0, verbose_name='错误次数'),
        ),
    ]
