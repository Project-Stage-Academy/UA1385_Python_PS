from django.shortcuts import render
from rest_framework import viewsets
from .models import StartupProfile
from .serializers import StartupProfileSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

class StartupProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'industry', 'description', 'address']
    ordering_fields = ['title', 'industry']

    @extend_schema(
        summary="Get list of startups",
        description="🔒 Returns all startups. Access only for authorized users.",
        responses={200: StartupProfileSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Startup Details",
        description="🔒 View detailed information about a single startup profile. Access is restricted to authorized users only.",
        responses={200: StartupProfileSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)