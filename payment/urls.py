from django.urls import path
from .views import payment_success

app_name='payment'

urlpatterns = [
    path('payment-success', payment_success, name='payment_success'),
]