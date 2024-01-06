from django.db import models
from django.contrib.auth.models import User

from Products.models import Product

# Create your models here.

class Cart(models.Model):
    session_key = models.CharField(max_length=32, unique=True)
    date_added = models.DateField(auto_now_add=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='items')
    quantity = models.IntegerField(null=True, default=0)
    is_checked_out = models.BooleanField(default=False)
