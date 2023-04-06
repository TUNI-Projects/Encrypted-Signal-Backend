import os
from django.db import models
from user.models import User
from uuid import uuid4


def update_filename(instance, filename):
    path="files/"
    format = "{}_{}".format(uuid4(), filename)
    return os.path.join(path, format)

# Create your models here.
class FileModel(models.Model):
    index = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    original_filename = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=update_filename)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_owner = models.ForeignKey(User, on_delete=models.PROTECT)