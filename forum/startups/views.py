from django.shortcuts import render
from rest_framework import viewsets
from .models import StartupProfile
from .serializers import StartupProfileSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

class StartupProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'industry', 'description', 'address']
    ordering_fields = ['title', 'industry']