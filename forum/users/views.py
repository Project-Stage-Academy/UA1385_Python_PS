from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer,LogoutSerializer
import logging
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self, request):
        logger.info("Received registration request")

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"New user registered successfully: id={user.user_id}, email={user.email}")
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        
        logger.warning(f"User registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response({"detail": "Logout successful."}, status=status.HTTP_204_NO_CONTENT)