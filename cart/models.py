from django.db import models
from django.contrib.auth.models import User

from Products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateField(auto_now_add=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='items')
    quantity = models.IntegerField(null=True, default=0)
    is_active = models.BooleanField(default=True)

