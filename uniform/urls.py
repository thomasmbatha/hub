from django.urls import path
from . import views

urlpatterns = [
    path('uniform/', views.uniform, name='uniform'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart-json/', views.cart_json, name='cart_json'),
    
]