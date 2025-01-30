# users/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404
from .models import UserModel
from .serializers import UserSerializer
import logging
from django.conf import settings
from django.http import FileResponse, JsonResponse
import os

logger = logging.getLogger(__name__)

@api_view(['POST'])
def add_user(request):
    """
    Add a new user to the database.
    Equivalent to /user/add in FastAPI.
    """
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"Created new user ID: {user.id}")
            return Response(
                {"id": user.id, "message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return Response({"detail": "Error creating user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_users(request):
    """
    Get all users from the database.
    Equivalent to /user/all in FastAPI.
    """
    try:
        users = UserModel.objects.all()  # or get_list_or_404(UserModel)
        serializer = UserSerializer(users, many=True)
        logger.info("Retrieved all users")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        return Response({"detail": "Error retrieving users"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def root_view(request):
    """
    Serve the React UI or a default message based on the SERVE_UI flag.
    Equivalent to FastAPI's "/" route.
    """
    if settings.SERVE_UI:
        # e.g. "path/to/app/frontend/build/index.html"
        react_index = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'index.html')
        print(react_index)
        if os.path.exists(react_index):
            return FileResponse(open(react_index, 'rb'))
        else:
            return JsonResponse({"detail": "React build not found. SERVE_UI is enabled but no build folder present."},
                                status=404)
    else:
        return JsonResponse({"message": "Django User Manager API is running. UI is disabled."})