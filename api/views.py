# samples/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404
from .models import SampleModel
from .serializers import SampleSerializer
import logging
from django.conf import settings
from django.http import FileResponse, JsonResponse
import os
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken
import requests  # Use Python's requests library instead of google.auth.transport.requests

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_sample(request):
    """
    Add a new sample to the database.
    Equivalent to /sample/add in FastAPI.
    """
    try:
        serializer = SampleSerializer(data=request.data)
        if serializer.is_valid():
            sample = serializer.save()
            logger.info(f"Created new sample ID: {sample.id}")
            return Response(
                {"id": sample.id, "message": "sample created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error creating sample: {str(e)}")
        return Response({"detail": "Error creating sample"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_samples(request):
    """
    Get all sample from the database.
    Equivalent to /sample/all in FastAPI.
    """
    # print user info
    print(request.user)
    try:
        samples = SampleModel.objects.all()  # or get_list_or_404(sampleModel)
        serializer = SampleSerializer(samples, many=True)
        logger.info("Retrieved all samples")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error retrieving samples: {str(e)}")
        return Response({"detail": "Error retrieving samples"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return JsonResponse({"message": "Django sample Manager API is running. UI is disabled."})

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    google_token = request.data.get('token')
    if not google_token:
        return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Use the access token to get user info from Google
        userinfo_response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {google_token}'}
        )
        
        if userinfo_response.status_code != 200:
            return Response(
                {'error': f'Failed to get user info from Google: {userinfo_response.text}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        userinfo = userinfo_response.json()
        print("Google user info:", userinfo)  # Debug print
        
        # Extract user info from the userinfo response
        email = userinfo.get('email')
        if not email:
            return Response({'error': 'Email not found in user info'}, status=status.HTTP_400_BAD_REQUEST)

        first_name = userinfo.get('given_name', '')
        last_name = userinfo.get('family_name', '')
        sub = userinfo.get('sub')  # This is the Google user ID
        
        if not sub:
            return Response({'error': 'User ID not found in Google response'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create user
        try:
            user = User.objects.get(email=email)
            # Update user info in case it changed
            if first_name or last_name:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        
        # Create or update social account
        SocialAccount.objects.update_or_create(
            user=user,
            provider='google',
            uid=sub,
            defaults={'extra_data': userinfo}
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
        
    except requests.RequestException as e:
        print("Google login error:", str(e))  # Add debug logging
        return Response(
            {'error': f'Failed to communicate with Google: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        print("Unexpected error during Google login:", str(e))  # Add debug logging
        return Response(
            {'error': f'Authentication failed: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )