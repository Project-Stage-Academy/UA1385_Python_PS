import logging
from rest_framework.permissions import BasePermission, IsAuthenticated

logger = logging.getLogger(__name__)

# # example of logging calls for future permissions

# class CustomPermission(BasePermission):
#     def has_permission(self, request, view):
#         if some_condition_fails:
#             logger.warning(f"Permission denied for user {request.user}")
#             return False
#         return True

class IsStartupRole(BasePermission):
    """
    Gives access to users with startup role. 
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or 2 not in getattr(user, 'roles', []):
            logger.warning(f"Permission denied for user {user} (not Startup)")
            return False
        return True
    
class IsInvestorRole(BasePermission):
    """
    Gives access to users with investor role.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or 1 not in getattr(user, 'roles', []):
            logger.warning(f"Permission denied for user {user} (not Investor)")
            return False
        return True