from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from django.core.paginator import Paginator
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def store(request, category_slug=None):
    
    searchItem = request.GET.get('searchItem')
    if request.GET:
        if searchItem:
            foods = Product.objects.filter(product_name__icontains=searchItem, is_discount=False)
        else:
            foods = Product.objects.all()
        context = {'searchItem': searchItem, 'foods': foods}
        return render(request, 'store/store.html', context)
        
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(is_available=True, category=category, is_discount=False)  # Category wise products
 
    else:
        # pass
        products = Product.objects.filter(is_available = True, is_discount=False)  # All products
    
    categories = Category.objects.all()
    context = {'foods': products, 'categories': categories}

    return render(request, 'store/store.html', context)
    



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
    


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    reviews = ReviewRating.objects.filter(product_id=single_product.id)

    context = {
        'product': single_product,
        'reviews': reviews
    }
    return render(request, 'store/product_detail.html', context)
    
    

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review_rating = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review_rating)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
            else:
                messages.error(request, 'Failed to update the review. Please check your input.')
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
            else:
                messages.error(request, 'Failed to submit the review. Please check your input.')


    product = get_object_or_404(Product, id=product_id)
    product_slug = product.slug
    category_slug = product.category.slug

    return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
        
    

def create_review(request, product_id):
    
    if request.method == 'POST':
        task = ReviewForm(request.POST)
        if task.is_valid():
            task.save()
            return redirect('products_by_category')
    else:
        task = ReviewForm()
    return render(request, 'reviewform.html', {'task': task})
