# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-09 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0049_auto_20180209_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationpaperitem',
            name='question_value',
            field=models.PositiveIntegerField(),
        ),
    ]