from django.urls import path
from .views import store, product_detail, submit_review, discount_store, discount_product_detail
# from .views import store, product_detail, rate_product, review_product, create_review

urlpatterns = [
    path('', store, name = 'store'),
    path('discount/', discount_store, name = 'discount_store'),
    
    path('category/<slug:category_slug>/', store, name = 'products_by_category'),
    path('discount/<slug:category_slug>/', discount_store, name = 'discount_products_by_category'),
    
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name = 'product_detail'),
    path('discount/<slug:category_slug>/<slug:product_slug>/', discount_product_detail, name = 'discount_product_detail'),
    
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),
    
]