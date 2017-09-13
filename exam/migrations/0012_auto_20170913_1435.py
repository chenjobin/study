# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-13 06:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0011_wronganswerinfo_object_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleWrongAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wrong_answer', models.CharField(default='', max_length=200, verbose_name='用户答案')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Single_Q', verbose_name='题目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='归属用户')),
            ],
            options={
                'verbose_name': '错题本_单选题',
                'verbose_name_plural': '错题本_单选题',
            },
        ),
        migrations.RemoveField(
            model_name='wronganswerinfo',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='wronganswerinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='WrongAnswerInfo',
        ),
    ]
