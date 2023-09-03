from django.urls import path
from .views import order_complete, place_order, success_view, full_order_complete, my_orders, order_view

urlpatterns = [
    path('order_complete/', order_complete, name='order_complete'),
    path('place_order/', place_order, name='place_order'),
    path('full_order_complete/', full_order_complete, name='full_order_complete'),
    path('success/', success_view, name='success_view'),
    path('my_orders/', my_orders, name='my_orders'),
    path('order_view/<str:t_no>', order_view, name='order_view'),
    
]
