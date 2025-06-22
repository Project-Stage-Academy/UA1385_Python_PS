from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvestorProfileViewSet

router = DefaultRouter()
router.register(r'', InvestorProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]