from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Exists, OuterRef
from projects.models import Project
from .models import Startup
from .serializers import StartupSerializer
from users.permissions import IsInvestor
from .filters import StartupFilter


class StartupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    filterset_class = StartupFilter
    # permission_classes = [IsAuthenticated, IsInvestor]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['industry', 'company_size', 'investment_needs']
    search_fields = ['title', 'description']