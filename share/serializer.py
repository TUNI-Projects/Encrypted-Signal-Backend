from rest_framework.serializers import ModelSerializer
from .models import FileModel, ShareModel


class UploadSerializer(ModelSerializer):

    class Meta:
        model = FileModel
        fields = ['encrypted_data', 'original_filename', 'file_owner', 'file_type']


class ShareSerializer(ModelSerializer):

    class Meta:
        model = ShareModel
        fields = "__all__"
