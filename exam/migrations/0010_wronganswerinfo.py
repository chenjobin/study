# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 09:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0009_auto_20170830_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='WrongAnswerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wrong_answer', models.CharField(default='', max_length=200, verbose_name='用户答案')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='归属用户')),
            ],
            options={
                'verbose_name': '错题本',
                'verbose_name_plural': '错题本',
            },
        ),
    ]