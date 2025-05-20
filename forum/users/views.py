from django.shortcuts import render
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

# Create your views here.

# example of logging calls for future views
"""
def example_view(self, request):
    try:
        # some processing/actions with data
        logger.info(f"Processing request")
        # returning responce
    except Exception as e:
        logger.error(f"Error occured: {e}")
        # returning responce
"""

#TODO : replace ExampleView with actual views

class ExampleView(APIView):
    def get(self, request):
        try:
            logger.info("Processing GET request in ExampleView")
            return Response({"message": "Success"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occurred in ExampleView: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)