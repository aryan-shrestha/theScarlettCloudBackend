from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from Products.models import Product
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
# Create your views here.

class CartDetail(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        return Cart.objects.get(user__id=user_id)


# The CartOperationsView is an API view that inherits from generics.CreateAPIView. It handles both adding items to the cart and modifying item quantities based on the operation parameter.
# The create method is used for adding items to the cart with a specified quantity.
# The patch method is used for increasing or decreasing the quantity of items in the cart based on the operation parameter. If the quantity becomes less than 1, the item is removed from the cart.
class CartOperationsView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        # If the item already exists in the cart, update the quantity
        cart_item.quantity += quantity
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def patch(self, request, *args, **kwargs):
        user = request.user
        
        operation = request.data.get('operation')
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item = CartItem.objects.filter(cart__user=user, product=product).first()

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
            return Response({"detail": "Invalid operation"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)