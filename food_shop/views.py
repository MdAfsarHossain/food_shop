from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category

def home(request, category_slug=None):
    
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(is_available=True, category=category, is_discount=False)  # Category wise products
        
    else:
        products = Product.objects.filter(is_available = True, is_discount=False)  # All products
    
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories, }
    
    return render(request, 'index.html', context)
    
 