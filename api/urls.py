# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/add', views.add_sample, name='add_user'),
    path('api/all', views.get_all_samples, name='all_users'),
    path('', views.root_view, name='root_view'),
    path('auth/google/', views.google_login, name='google_login'),
]
