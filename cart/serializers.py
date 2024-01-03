from rest_framework.serializers import ModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer

from cart.models import CartItem, Cart
from Products.serializers import ProductSerializer

class CartItemSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'is_active']

class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'
