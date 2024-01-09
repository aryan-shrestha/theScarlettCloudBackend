from django.urls import path

from .views import InitiateKhaltiPayment, VerifyKhaltiPayment, OrderDetailView

urlpatterns = [
    path('', OrderDetailView.as_view(), name='order_detail'),
    path('khalti-initiate/', InitiateKhaltiPayment.as_view(), name='initiate_khalti_payment'),
    path('verify-khalti-payment/', VerifyKhaltiPayment.as_view(), name='verify_khalti_payment'),
]