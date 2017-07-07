from __future__ import unicode_literals

from django.db import models


def comp_upload_path(instance, filename):
    return "{0}/{1}".format(instance.root_dir, filename)


class Document(models.Model):
    root_dir = models.CharField(max_length=300)
    doc_file = models.FileField(upload_to=comp_upload_path)

