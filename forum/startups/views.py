from rest_framework import viewsets, filters, generics, mixins
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Startup
from .serializers import StartupSerializer
from users.permissions import IsInvestor, IsInvestorOrOwner
from .filters import StartupFilter

class StartupViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    filterset_class = StartupFilter
    permission_classes = [IsAuthenticated, IsInvestorOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['industry', 'company_size', 'investment_needs']
    search_fields = ['title', 'description']