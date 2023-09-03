from django.urls import path
from .views import cart, add_to_cart, remove_cart, remove_cart_item

urlpatterns = [
    path('', cart, name = 'cart'),
    path('<int:product_id>/', add_to_cart, name = 'add_cart'),
    path('remove/<int:product_id>/<int:cart_item_id>', remove_cart_item, name = 'remove_cart_item'),
    path('delete/<int:product_id>/<int:cart_item_id>', remove_cart, name= 'remove_cart'),
]