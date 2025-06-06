from rest_framework import serializers
from .models import StartupProfile

class StartupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupProfile
        fields = '__all__'
    
    def validate_company_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Company name cannot be empty.")
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description is required.")
        return value