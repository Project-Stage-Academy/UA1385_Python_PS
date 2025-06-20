from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
import logging
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

logger = logging.getLogger(__name__)

@extend_schema(
    tags=["users"],
    summary="Login"
)
class LoginView(TokenObtainPairView):
    pass

@extend_schema(tags=["users"])
class RefreshView(TokenRefreshView):
    pass
@extend_schema(
    tags=["users"],
    summary="Create a new user"
)
class RegisterView(APIView):

    def post(self, request):
        logger.info("Received registration request")

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except Exception as e:
                logger.error(f"Error while saving user: {e}")
                return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            logger.info(f"New user registered successfully: id={user.user_id}, email={user.email}")
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        
        logger.warning(f"User registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

