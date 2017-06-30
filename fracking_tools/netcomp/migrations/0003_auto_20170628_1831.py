# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 01:31
from __future__ import unicode_literals

from django.db import migrations, models
import netcomp.models


class Migration(migrations.Migration):

    dependencies = [
        ('netcomp', '0002_auto_20170628_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvdocument',
            name='root_dir',
            field=models.CharField(default='csv_files', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='csvdocument',
            name='csv_file',
            field=models.FileField(upload_to=netcomp.models.csv_upload_path),
        ),
    ]