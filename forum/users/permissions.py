import logging
from rest_framework.permissions import BasePermission, SAFE_METHODS

logger = logging.getLogger(__name__)

# # example of logging calls for future permissions

# class CustomPermission(BasePermission):
#     def has_permission(self, request, view):
#         if some_condition_fails:
#             logger.warning(f"Permission denied for user {request.user}")
#             return False
#         return True

class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 1

class IsStartup(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 2

class IsInvestorOrOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated and request.user.role == 1
        return request.user.is_authenticated and request.user.role == 2

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.role == 1
        return obj.user_id == request.user
