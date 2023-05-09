import os
from django.db import models
from user.models import User
from uuid import uuid4


def update_filename(instance, filename):
    path = "files/"
    format = "{}".format(uuid4())
    return os.path.join(path, format)

# Create your models here.


class FileModel(models.Model):
    index = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    original_filename = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=update_filename, blank=True)
    encrypted_data = models.TextField(null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_owner = models.ForeignKey(User, on_delete=models.PROTECT)
    file_type = models.CharField(max_length=255, blank=True)


class ShareModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.PROTECT)
    shared_on = models.DateTimeField(auto_now_add=True)
