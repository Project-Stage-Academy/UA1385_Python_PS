from django.urls import path
from .views import ExampleView

urlpatterns = [
    #TODO : replace this exeample path with actual paths
    path("logtest/", ExampleView.as_view(), name="logtest"),
]