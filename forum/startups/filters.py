import django_filters
from .models import Startup

class StartupFilter(django_filters.FilterSet):
    investment_needs = django_filters.BooleanFilter(method='filter_investment_needs')

    class Meta:
        model = Startup
        fields = ['industry', 'company_size']

    def filter_investment_needs(self, queryset, name, value):
        if value:
            return queryset.filter(project__progress=True).distinct()
        else:
            return queryset.exclude(project__progress=True).distinct()