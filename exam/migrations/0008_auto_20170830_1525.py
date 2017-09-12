# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 07:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_auto_20170829_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fill_Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(default='', max_length=200, verbose_name='正确答案')),
            ],
            options={
                'verbose_name': '填空题答案',
                'verbose_name_plural': '填空题答案',
            },
        ),
        migrations.RemoveField(
            model_name='fill_q',
            name='answer',
        ),
        migrations.AlterField(
            model_name='fill_q',
            name='blank_num',
            field=models.PositiveIntegerField(default=1, verbose_name='空白数'),
        ),
        migrations.AddField(
            model_name='fill_answer',
            name='fill_q',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Fill_Q', verbose_name='归属填空题'),
        ),
    ]