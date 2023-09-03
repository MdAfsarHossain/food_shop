from django.urls import path
from .views import discount_store, discount_product_detail

urlpatterns = [
    path('', discount_store, name = 'discount_store'),
    
    path('discount/<slug:category_slug>/', discount_store, name = 'discount_products_by_category'),
    path('discount/<slug:category_slug>/<slug:product_slug>/', discount_product_detail, name = 'discount_product_detail'),
    
]