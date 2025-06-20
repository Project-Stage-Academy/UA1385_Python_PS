from django.shortcuts import render
from rest_framework import viewsets

from .models import StartupProfile, Subscription
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import StartupProfileSerializer
from users.permissions import IsStartupRole, IsInvestorRole
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    tags=["startups"],
    summary="Startup Profile ViewSet",
    description="ViewSet to manage startup profiles. Requires authentication."
)

class StartupProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'industry', 'description', 'address']
    ordering_fields = ['title', 'industry']

    @extend_schema(
        summary="Get list of startups",
        description="Returns all startup profiles. Access only for authorized users.",
        responses={
            200: StartupProfileSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized: Authentication credentials were not provided.")
        }
    )
    def list(self, request, *args, **kwargs):
        """
            Retrieve a list of all startup profiles.

            Responses:
            - 200 OK: Successfully returns a list of startup profiles.
            - 401 Unauthorized: Authentication credentials were not provided.
            """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Startup Details",
        description="View detailed information about a single startup profile. Access is restricted to authorized users only.",
        responses={
            200: StartupProfileSerializer,
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not Found: Startup profile does not exist.")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information about a startup profile by ID.

        Responses:
        - 200 OK: Returns startup profile data.
        - 401 Unauthorized: Authentication credentials were not provided.
        - 404 Not Found: Startup profile does not exist.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new startup profile",
        description="Only for authorized users with role=2 (startup). Creates a new profile.",
        request=StartupProfileSerializer,
        responses={
            201: StartupProfileSerializer,
            400: OpenApiResponse(description="Bad Request: Profile already exists or invalid data."),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new startup profile. Only one profile per user is allowed.

        Restrictions:
        - Only users with role=2 (startup) can create.
        - A user can have only one startup profile.

        Request Body:
        - title(str): The name of the startup.
        - description(str): The description of the startup.
        - industry(str): The industry of the startup.
        - website(str): The website URL of the startup.
        - address(str): The contact email for the startup.

        Responses:
        - 201 Created: Successfully creates the startup profile.
        - 400 Bad Request: Profile already exists or invalid input data.
        - 401 Unauthorized: Authentication credentials were not provided.
        - 403 Forbidden: Access denied.
        """
        if request.user.role != 2:
            return Response(
                {"detail": "Only users with role=2 can create startup profiles."},
                status=403
            )
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a startup profile (PUT)",
        description="Replaces the entire startup profile.",
        request=StartupProfileSerializer,
        responses={
            200: StartupProfileSerializer,
            400: OpenApiResponse(description="Bad Request: Invalid input data."),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Replace an existing startup profile with new data.

        Responses:
        - 200 OK: Successfully updated.
        - 400 Bad Request: Invalid input.
        - 401 Unauthorized: Authentication required.
        - 403 Forbidden: Access denied.
        - 404 Not Found: Profile not found.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update of a startup profile (PATCH)",
        description="Partially updates a startup profile.",
        request=StartupProfileSerializer,
        responses={
            200: StartupProfileSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a startup profile.

        Responses:
        - 200 OK: Successfully updated.
        - 400 Bad Request: Invalid input.
        - 401 Unauthorized: Authentication required.
        - 403 Forbidden: Access denied.
        - 404 Not Found: Profile not found.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a startup profile",
        description="Permanently deletes a startup profile.",
        responses={
            204: OpenApiResponse(description="No content: Successfully deleted."),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not Found")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a startup profile.

        Responses:
        - 204 No Content: Successfully deleted.
        - 401 Unauthorized: Authentication required.
        - 403 Forbidden: Access denied.
        - 404 Not Found: Profile not found.
        """
        return super().destroy(request, *args, **kwargs)

    
    def get_permissions(self):
        # Startup Only
        startup_only_actions = ['create', 'update', 'partial_update', 'destroy']
        if self.action in startup_only_actions:
            return [IsAuthenticated(), IsStartupRole()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsInvestorRole])
    def subscribe(self, request, pk=None):
        startup = self.get_object()
        subscription, created = Subscription.objects.get_or_create(
            investor=request.user,
            startup=startup
        )
        if created:
            return Response({"status": "subscribed"}, status=201)
        return Response({"status": "already subscribed"}, status=200)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsInvestorRole])
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
