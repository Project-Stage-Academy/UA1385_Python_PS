from django.shortcuts import render
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