from django.db import models
from decimal import Decimal

class User(models.Model):
    """
    This model is for user registration
    Attributes
    first_name: This attribute holds the first name of the user
    last_name: This attribute holds the last name of the user
    email: This attribute holds the email of the user
    """
    user_id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.first_name
