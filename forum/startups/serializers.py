from rest_framework import serializers
from .models import StartupProfile

class StartupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupProfile
        fields = '__all__'
    
    def validate_startup_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Startup title cannot be empty.")
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description is required.")
        return value