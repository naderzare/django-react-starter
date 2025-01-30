# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/add', views.add_user, name='add_user'),
    path('api/all', views.get_all_users, name='all_users'),
    path('', views.root_view, name='root_view'),
]
