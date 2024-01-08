from django.urls import path

from cart.views import CartDetail, CartOperationsView, CartItemDeleteView
urlpatterns = [
    path('', CartDetail.as_view(), name='cart-detail'),
    path('cart-operations/', CartOperationsView.as_view(), name='cart-operations'),
    path('cart-operations/<int:pk>/', CartItemDeleteView.as_view(), name='cart-operations-delete')
]