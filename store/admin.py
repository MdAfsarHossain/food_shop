from django.contrib import admin
from . models import Product, ReviewRating

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category', 'stock', 'created_date', 'modified_date', 'is_available', 'is_discount']
    prepopulated_fields = {'slug': ('product_name', )}
    
admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)


