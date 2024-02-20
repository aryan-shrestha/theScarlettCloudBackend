from django.urls import path

from .views import InitiateKhaltiPayment, VerifyKhaltiPayment, OrderDetailView, OrderListView

urlpatterns = [
    path('', OrderDetailView.as_view(), name='order_detail'),
    path('list/', OrderListView.as_view(), name='order_list'),
    path('khalti-initiate/', InitiateKhaltiPayment.as_view(), name='initiate_khalti_payment'),
    path('verify-khalti-payment/', VerifyKhaltiPayment.as_view(), name='verify_khalti_payment'),
]