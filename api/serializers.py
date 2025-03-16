# users/serializers.py
from rest_framework import serializers
from .models import SampleModel, UserAccount, PaymentTransaction
from django.contrib.auth.models import User

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['id', 'name', 'age']

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'account_value', 'last_updated']

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'transaction_id', 'amount', 'currency', 'status', 'payment_method', 'created_at']

class UserWithAccountSerializer(serializers.ModelSerializer):
    account = UserAccountSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'account']
