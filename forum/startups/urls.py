from django.urls import path, include
from .views import StartupViewSet

# router = DefaultRouter()
# router.register(r'startups', StartupViewSet, basename='startup')

startup_detail = StartupViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})

urlpatterns = [
    path('', StartupViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', startup_detail),
]