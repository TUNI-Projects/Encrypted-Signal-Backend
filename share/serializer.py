from rest_framework.serializers import ModelSerializer
from .models import FileModel

class UploadSerializer(ModelSerializer):
    
    
    class Meta:
        model = FileModel
        fields = ['file', 'original_filename', 'file_owner']