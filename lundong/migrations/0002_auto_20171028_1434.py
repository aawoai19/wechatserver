# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lundong', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zhishu',
            name='name_id',
            field=models.BigIntegerField(),
        ),
    ]
