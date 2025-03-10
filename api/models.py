# users/models.py
from django.db import models

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