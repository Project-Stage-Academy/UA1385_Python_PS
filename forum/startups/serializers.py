from rest_framework import serializers
from .models import Startup

class StartupSerializer(serializers.ModelSerializer):
    investment_needs = serializers.SerializerMethodField()

    class Meta:
        model = Startup
        fields = [
            'startup_id', 'title', 'description', 'industry',
            'company_size', 'investment_needs', 'website', 'address'
        ]
        read_only_fields = ['startup_id', 'user_id']

    def get_investment_needs(self, obj):
        return obj.investment_needs
