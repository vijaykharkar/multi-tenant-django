from rest_framework import serializers
from .models import Tenant_User
from django.contrib.auth.models import User

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant_User
        fields = '__all__'



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already exists.")
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email already exists.")
        return data
    
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
 


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        