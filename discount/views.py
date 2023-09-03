from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, ReviewRating
from category.models import Category
from django.core.paginator import Paginator
from store.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def discount_store(request, category_slug=None):
    
    searchItem = request.GET.get('searchItem')
    if request.GET:
        if searchItem:
            foods = Product.objects.filter(product_name__icontains=searchItem, is_discount=True)
        else:
            foods = Product.objects.all()
        context = {'searchItem': searchItem, 'foods': foods}
        return render(request, 'store/discount_store.html', context)
        
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(is_available=True, category=category, is_discount=True)  # Category wise products
 
    else:
        # pass
        products = Product.objects.filter(is_available = True, is_discount=True)  # All products
    
    categories = Category.objects.all()
    context = {'foods': products, 'categories': categories}

    return render(request, 'store/discount_store.html', context)
    


def discount_product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    reviews = ReviewRating.objects.filter(product_id=single_product.id)

    context = {
        'product': single_product,
        'reviews': reviews
    }
    return render(request, 'store/discount_product_detail.html', context)
    
