from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StartupProfileViewSet

router = DefaultRouter()
router.register(r'', StartupProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]