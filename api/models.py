# users/models.py
from django.db import models
from django.contrib.auth.models import User

class SampleModel(models.Model):
    """
    Database model for storing user info.
    """
    name = models.CharField(max_length=150, db_index=True)
    age = models.IntegerField()

    # By default, Django creates an "id" primary key
    # so no need to explicitly declare it unless you want a custom field name.

    def __str__(self):
        return f"{self.name} ({self.age})"

class UserAccount(models.Model):
    """
    Database model for storing user account details such as account value
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s account (${self.account_value})"
    
class PaymentTransaction(models.Model):
    """
    Database model for storing payment transaction details
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, default='pending')  # pending, completed, failed
    payment_method = models.CharField(max_length=50, default='lemon_squeezy')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.user.username} - ${self.amount}"