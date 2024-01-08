from rest_framework.serializers import ModelSerializer

from cart.models import CartItem, Cart
from Products.models import Product, ProductImages
from Products.serializers import ProductImageSerializer
from category.serializers import CategorySerializer

class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'og_price', 'dis_price', 'images', 'category']

class CartItemSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'is_checked_out']

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'session_key', 'date_added', 'total']
