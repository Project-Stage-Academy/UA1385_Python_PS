from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
import logging


logger = logging.getLogger(__name__)

# Create your views here.

# # example of logging calls for future views
#
# def example_view(self, request):
#     try:
#         # some processing/actions with data
#         logger.info(f"Processing request")
#         # returning responce
#     except Exception as e:
#         logger.error(f"Error occured: {e}")
#         # returning responce

@extend_schema(
    tags=["projects"]
)
class ProjectProfileViewSet(viewsets.ModelViewSet):
    pass