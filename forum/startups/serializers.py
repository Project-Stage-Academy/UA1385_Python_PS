from rest_framework import serializers
from .models import Startup

class StartupSerializer(serializers.ModelSerializer):
    investment_needs = serializers.SerializerMethodField()

    class Meta:
        model = Startup
        fields = [
            'id', 'title', 'description', 'industry',
            'company_size', 'investment_needs', 'website', 'address'
        ]

    def get_investment_needs(self, obj):
        return obj.investment_needs