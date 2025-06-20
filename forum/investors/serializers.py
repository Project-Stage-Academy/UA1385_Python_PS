from rest_framework import serializers
from .models import InvestorProfile

class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = '__all__'
        read_only_fields = ['investor_id', 'user_id', 'created_at']