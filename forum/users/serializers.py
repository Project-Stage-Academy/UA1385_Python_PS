from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from startups.models import Startup

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'user_name', 'first_name', 'last_name', 'role', 'title', 'user_phone']


    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_user_name(self, value):
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if user.role == 2:
            Startup.objects.create(user_id=user)
        return user


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_name']