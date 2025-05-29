from django.urls import path
from .views import cart_summary, cart_add, cart_update, cart_delete

app_name = 'cart'

urlpatterns = [
    path('', cart_summary, name='cart_summary'),
    path('cart-add/', cart_add, name='cart_add'),
    path('cart-update/', cart_update, name='cart_update'),
    path('cart-delete/', cart_delete, name='cart_delete')
]

