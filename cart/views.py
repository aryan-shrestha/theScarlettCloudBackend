from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from Products.models import Product
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
# Create your views here.

def get_session_id(request):
    session_id = request.session.session_key
    if session_id == None:
        request.session.save()
        session_id = request.session.session_key
    
    return session_id

class CartDetail(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # retrieve the user's cart based on the session key
        
        session_key = get_session_id(self.request)
        queryset = Cart.objects.filter(session_key=session_key)

        if queryset.exists():
            return queryset.first()
        else:
            return Cart.objects.create(session_key=session_key)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cart_serializer = self.get_serializer(instance)
        cart_items = CartItem.objects.filter(cart=instance, is_checked_out=False)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        response_data = {
            "cart": cart_serializer.data,
            "cart_items": cart_items_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class CartOperationsView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        session_key = get_session_id(request)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()

        serializer = self.get_serializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        session_key = get_session_id(request)
        operation = request.data.get('operation')
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product does not exists'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item = CartItem.objects.filter(cart__session_key=session_key, product=product).first()
        
        if not cart_item:
            return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)

        if operation == 'increase':
            cart_item.quantity += 1
        elif operation == 'decrease':
            if cart_item.quantity <= 1:
                cart_item.delete()
                return Response({'detail': 'Item in cart deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                cart_item.quantity -= 1
        else:
            return Response({'detail': 'Invalid operation'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        session_key = get_session_id(request)
        cart_item_id = request.data.get('cart_item_id')
        
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Item not found in the cart'}, status=status.HTTP_404_NOT_FOUND)

        cart = cart_item.cart

        if session_key == cart.session_key:
            cart_item.delete()
            return Response({'detail': 'Cart item deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': "Invalid session id"}, status=status.HTTP_401_UNAUTHORIZED)
