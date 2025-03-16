# samples/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import SampleModel, UserAccount, PaymentTransaction
from .serializers import SampleSerializer, UserAccountSerializer, PaymentTransactionSerializer, UserWithAccountSerializer
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
import json
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from decimal import Decimal, InvalidOperation, InvalidOperation

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
            username = email
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
            
            # Create user account with default value
            UserAccount.objects.create(user=user, account_value=0.00)
        
        # Create or update social account
        SocialAccount.objects.update_or_create(
            user=user,
            provider='google',
            uid=sub,
            defaults={'extra_data': userinfo}
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Make sure user has an account
        account, created = UserAccount.objects.get_or_create(user=user, defaults={'account_value': 0.00})
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'account_value': float(account.account_value)
        }
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_data
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_account(request):
    """
    Get the current user's account details
    """
    try:
        # Get or create user account
        account, created = UserAccount.objects.get_or_create(
            user=request.user, 
            defaults={'account_value': 0.00}
        )
        
        serializer = UserAccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error retrieving user account: {str(e)}")
        return Response({"detail": "Error retrieving user account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    """
    Create a payment intent (transaction) and return a checkout URL
    """
    try:
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        products_lookup = get_product_list()
        
        if not products_lookup:
            logger.error("Failed to fetch products list")
            return Response({"detail": "Failed to fetch products list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Find the product in the list by matching ID
        product_info = next((item for item in products_lookup if item["id"] == product_id), None)
        if not product_info:
            logger.error(f"Invalid product_id received: {product_id}")
            return Response({"detail": "Invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the price string (removing currency symbol and converting to decimal)
        price_str = product_info["price"]
        # Remove currency symbol, commas and any whitespace
        price_str = ''.join(c for c in price_str if c.isdigit() or c == '.')
        
        try:
            amount = Decimal(price_str)
        except (InvalidOperation, ValueError) as e:
            logger.error(f"Failed to parse price string '{price_str}': {str(e)}")
            return Response(
                {"detail": "Invalid price format from product data"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Create a local transaction with 'pending' status
        transaction = PaymentTransaction.objects.create(
            user=request.user,
            transaction_id=f"ls_{os.urandom(8).hex()}",  # Random transaction ID
            amount=amount,
            status='pending', 
            currency='CAD'  # Adjust as needed
        )

        # Build the Lemon Squeezy checkout URL with custom data
        checkout_url = (
            f"{product_info['by_now_url']}?"
            f"checkout[custom][transaction_id]={transaction.transaction_id}"
        )

        return Response({
            "transaction_id": transaction.transaction_id,
            "checkout_url": checkout_url,
            "amount": float(transaction.amount),
            "status": transaction.status,
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.error(f"Error creating payment intent: {str(e)}", exc_info=True)
        return Response(
            {"detail": "Error creating payment intent"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@csrf_exempt
@require_POST
@api_view(['POST'])
@permission_classes([AllowAny])
def lemon_squeezy_webhook(request):
    """
    Handle Lemon Squeezy webhooks
    """
    try:
        logger.debug(f"Received webhook request. Headers: {dict(request.headers)}")
        logger.debug(f"Request body: {request.body.decode('utf-8')}")

        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse webhook JSON: {str(e)}")
            return Response({"detail": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST)

        signature = request.headers.get('X-Signature')
        if not signature:
            logger.error("Missing X-Signature header")
            return Response({"detail": "Missing signature"}, status=status.HTTP_401_UNAUTHORIZED)

        # Verify the webhook signature (implement real check in production)
        if not verify_lemon_squeezy_signature(request.body, signature):
            logger.error("Invalid webhook signature")
            return Response({"detail": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)

        meta_data = payload.get('meta', {})
        event_name = meta_data.get('event_name')
        if not event_name:
            logger.error("Missing event_name in payload['meta']")
            return Response({"detail": "Missing event name"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Processing webhook event: {event_name}")

        # 1) Get custom_data from meta
        custom_data = meta_data.get('custom_data', {})
        if not isinstance(custom_data, dict):
            logger.error(f"Invalid custom_data format: {custom_data}")
            return Response({"detail": "Invalid custom_data format"}, status=status.HTTP_400_BAD_REQUEST)

        transaction_id = custom_data.get('transaction_id')
        if not transaction_id:
            logger.error("No transaction_id in meta.custom_data")
            return Response({"detail": "No transaction ID found"}, status=status.HTTP_400_BAD_REQUEST)

        # 2) Optionally, read from data->attributes if needed:
        order_data = payload.get('data', {}).get('attributes', {})
        order_status = order_data.get('status')
        # etc...

        # 3) Handle events
        if event_name == 'order_created':
            # Mark transaction as 'processing'
            try:
                transaction = PaymentTransaction.objects.get(transaction_id=transaction_id)
                transaction.status = 'processing'
                transaction.save()
                logger.info(f"Updated transaction {transaction_id} to processing status")
            except PaymentTransaction.DoesNotExist:
                logger.error(f"Transaction not found: {transaction_id}")
                return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        elif event_name == 'order_paid':
            # Mark transaction as 'completed' & update user balance
            try:
                transaction = PaymentTransaction.objects.get(transaction_id=transaction_id)
                transaction.status = 'completed'
                transaction.save()

                account, _ = UserAccount.objects.get_or_create(
                    user=transaction.user, defaults={'account_value': 0.00}
                )
                old_balance = account.account_value
                account.account_value += Decimal(str(transaction.amount))
                account.save()

                logger.info(f"Transaction {transaction_id} completed. "
                            f"Balance updated from {old_balance} to {account.account_value}")
            except PaymentTransaction.DoesNotExist:
                logger.error(f"Transaction not found: {transaction_id}")
                return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Error updating account balance: {str(e)}")
                return Response({"detail": "Error updating account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Unhandled event type: {event_name}")
            return Response({"detail": "Event acknowledged"}, status=status.HTTP_200_OK)

        return Response({"detail": "Webhook processed successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return Response({"detail": "Error processing webhook"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def verify_lemon_squeezy_signature(payload, signature):
    """
    Verify the Lemon Squeezy webhook signature using HMAC SHA256
    """
    if not signature:
        return False
    
    secret = settings.LEMON_SQUEEZY_SIGNING_SECRET
    # If secret is not configured, fail closed (secure by default)
    if not secret or secret == 'your-signing-secret':
        logger.error("Lemon Squeezy signing secret not properly configured")
        return False
        
    # Calculate expected signature
    calculated_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Use hmac.compare_digest for timing attack safe comparison
    return hmac.compare_digest(calculated_signature, signature)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_history(request):
    """
    Get the user's payment history
    """
    try:
        transactions = PaymentTransaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = PaymentTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error retrieving payment history: {str(e)}")
        return Response({"detail": "Error retrieving payment history"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def get_product_list():
    """
    Fetches the product list from Lemon Squeezy's API and returns a simplified list.
    """
    try:
        # 1) Load the API token from the environment
        api_token = os.getenv('LEMON_SQUEEZY_API_KEY', None)
        if not api_token:
            logger.error("LEMON_SQUEEZY_API_KEY not set in environment")
            return Response(
                {"detail": "Server misconfiguration: no API key."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 2) Request the product list from Lemon Squeezy API
        url = "https://api.lemonsqueezy.com/v1/products"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_token}",
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.error(f"Failed to fetch products: {response.text}")
            return Response(
                {"detail": f"Error fetching products from Lemon Squeezy. Status: {response.status_code}"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        data = response.json()
        products_list = []
        for item in data.get("data", []):
            attr = item.get("attributes", {})
            # Removed unnecessary print statements; build a cleaner product object
            products_list.append({
                # Extract product ID from the buy_now_url if available
                "id": attr.get("buy_now_url").split("/")[-1] if attr.get("buy_now_url") else None,
                "by_now_url": attr.get("buy_now_url"),
                "name": attr.get("name"),
                "slug": attr.get("slug"),
                "price": attr.get("price_formatted"),  # Consider using "from_price" if needed
            })

        logger.debug(f"Fetched {len(products_list)} products from Lemon Squeezy")
        return products_list
    except Exception as e:
        logger.exception("Unexpected error fetching Lemon Squeezy products")
        raise e
    
@api_view(['GET'])
@permission_classes([AllowAny])  # or IsAuthenticated if you want only logged-in users
def get_products(request):
    """
    Returns the product list as a JSON response.
    """
    try:
        products_list = get_product_list()
        logger.info(f"Returning {len(products_list)} products to client")
        return Response(products_list, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Unexpected error fetching Lemon Squeezy products")
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)