from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'user_name', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)