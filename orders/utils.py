from cart.models import CartItem
from orders.models import OrderItem

def move_cart_items_to_ordered_items(request, order, payment, cart_items):
    for cart_item in cart_items:
        order_item = OrderItem()
        order_item.order = order
        order_item.payment = payment
        order_item.product = cart_item.product
        order_item.quantity = cart_item.quantity
        order_item.ordered = True
        order_item.save()
        cart_item.delete()
