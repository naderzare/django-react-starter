# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/add', views.add_sample, name='add_user'),
    path('api/all', views.get_all_samples, name='all_users'),
    path('', views.root_view, name='root_view'),
    path('auth/google/', views.google_login, name='google_login'),
    
    # Payment-related endpoints - remove /api/ prefix as it's already included in backend/urls.py
    path('account/', views.get_user_account, name='user_account'),
    path('payments/create/', views.create_payment_intent, name='create_payment'),
    path('payments/history/', views.get_payment_history, name='payment_history'),
    path('webhooks/lemonsqueezy/', views.lemon_squeezy_webhook, name='lemon_squeezy_webhook'),
    # Add products list route
    path('payments/products/', views.get_products, name='get_products'),
]
