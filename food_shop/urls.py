from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf.urls.static import static
from django.conf import settings

from store.views import product_detail, discount_store

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('account/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('orders.urls')),
    path('discount/', include('discount.urls')),
    

    path('discount/<slug:category_slug>/', discount_store, name = 'discount_products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name = 'product_detail'),
    path('', include('food_app.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
