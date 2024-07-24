"""
This module contains the model definitions for the application.
"""

from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """
    Model representing a product.

    Attributes:
        user (User): The user who created the product.
        desc (str): The description of the product.
        price (Decimal): The price of the product.
        createdTime (DateTime): The timestamp when the product was created.
        image (ImageField): The image of the product.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    desc = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    createdTime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')
