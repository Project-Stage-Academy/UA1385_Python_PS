from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    roles = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'user_name', 'first_name', 'last_name', 'roles']


    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_user_name(self, value):
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        user = User.objects.create_user(**validated_data)
        user.roles = roles
        user.save()
        return user



class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_name']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    role = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        role = attrs.pop('role', None)
        data = super().validate(attrs)
        user = self.user

        if role is not None and role not in user.roles:
            raise serializers.ValidationError("User does not have this role.")

        role_display = dict(User.ROLES).get(role, "Unknown")
        data['logged_in_as'] = role_display
        return data