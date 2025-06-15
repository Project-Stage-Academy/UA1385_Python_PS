from django.shortcuts import render
from rest_framework import viewsets
from .models import StartupProfile, Subscription
from rest_framework.decorators import action
from rest_framework.response import Response
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
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        if request.user.role != 1:  # 1 — Investor
            return Response({"error": "Only investors can subscribe"}, status=403)
        startup = self.get_object()
        subscription, created = Subscription.objects.get_or_create(
            investor=request.user,
            startup=startup
        )
        if created:
            return Response({"status": "subscribed"}, status=201)
        return Response({"status": "already subscribed"}, status=200)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        startup = self.get_object()
        subscription = Subscription.objects.filter(
            investor=request.user,
            startup=startup
        )

        if subscription:
            subscription.delete()
            return Response({"status": "unsubscribed"}, status=200)
        else:
            return Response({"status": "not subscribed"}, status=400)