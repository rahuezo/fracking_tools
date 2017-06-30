from __future__ import unicode_literals

from django.db import models

def csv_upload_path(instance, filename):
    return "{0}/{1}".format(instance.root_dir, filename)

class CsvDocument(models.Model):
    root_dir = models.CharField(max_length=300)
    csv_file = models.FileField(upload_to=csv_upload_path)
    