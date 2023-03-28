from user.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email", "password", "username"]
    
    @staticmethod
    def validate_email(val):
        if User.objects.filter(email=val).count() >=1:
            raise serializers.ValidationError('Email {} is already in use!'.format(val))
        return val