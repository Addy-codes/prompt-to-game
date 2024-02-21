# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', CreateCheckoutSession.as_view(), name='checkout'),
    path('payment-success/', PaymentSuccess.as_view(), name='payment-success'),
    path('payment-failed/', PaymentFailed.as_view(), name='payment-failed'),
    path('webhook-test/', WebHook.as_view()),
]
