# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 11:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0025_auto_20170922_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fill_q',
            name='blank_num',
        ),
    ]
