# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-26 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pairwise_comparisons', '0002_auto_20170626_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='doc_file',
            field=models.FileField(upload_to='media'),
        ),
    ]
