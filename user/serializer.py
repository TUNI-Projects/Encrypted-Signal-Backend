from user.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email", "password", "username"]
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
     
    @staticmethod
    def validate_email(val):
        if User.objects.filter(email=val).count() >=1:
            raise serializers.ValidationError('Email {} is already in use!'.format(val))
        return val