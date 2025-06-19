from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import InvestorProfile
from .serializers import InvestorProfileSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["investors"]
)

class InvestorProfileViewSet(viewsets.ModelViewSet):
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 1:
            return Response({'detail': 'Only users with role=1 (Investor) can create investor profile.'},
                            status=status.HTTP_403_FORBIDDEN)

        if hasattr(request.user, 'investorprofile'):
            return Response({'detail': 'Profile already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
