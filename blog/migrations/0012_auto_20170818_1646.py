# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_entry_read_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='标签'),
        ),
    ]
