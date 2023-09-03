from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from .forms import OrderForm
from .models import Payment, OrderProduct, Order
from store.models import Product
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import random
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch') # csrf ke disable kore deoya
def success_view(request):
    data = request.POST
    
    user_id = int(data['value_b'])  # Retrieve the stored user ID as an integer
    user = User.objects.get(pk=user_id)
    payment = Payment(
        user = user,
        payment_id =data['tran_id'],
        payment_method = data['card_issuer'],
        amount_paid = int(data['store_amount'][0]),
        status =data['status'],
    )
    payment.save()
    
    # working with order model
    order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_a'])
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user = user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        product = Product.objects.get(id=item.product.id)
        orderproduct.order = order
        orderproduct.payment = payment
        orderproduct.user = user
        orderproduct.product = product
        orderproduct.quantity = item.quantity
        orderproduct.ordered = True
        orderproduct.save()

        # Reduce the quantity of the sold products
        
        product.stock -= item.quantity # order complete tai stock theke quantity komay dilam
        product.save()

    # Clear cart
    CartItem.objects.filter(user=user).delete()
    return redirect('cart')
    

def full_order_complete(request):
    return render(request, 'orders/order_complete.html')


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        # orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()



    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


@login_required
def order_complete(request):
    if request.method == 'POST': 
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        
        neworder.payment_mode = request.POST.get('payment_mode')
        
        tax = 0
        total = 0
        grand_total = 0
        cart = CartItem.objects.filter(user = request.user)
        
        if cart.count() < 1:
            return redirect('store')
        
        for item in cart:
            total += item.product.price * item.quantity
            
      
        
        tax = (2*total)/100 
        grand_total = total + tax
        
        neworder.order_total = grand_total
        
        trackno = 'afsar'+str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'afsar'+str(random.randint(1111111, 9999999))
            
        neworder.tracking_no = trackno
        neworder.save()
        
        
        
        neworderItems = CartItem.objects.filter(user = request.user)
        for item in neworderItems:
            OrderProduct.objects.create(
                order = neworder,
                product = item.product,
                quantity = item.quantity,
                price =grand_total,
                ordered=True
            )
            
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.stock -= item.quantity
            orderproduct.save()
            
        CartItem.objects.filter(user=request.user).delete()
        
        
    return redirect('full_order_complete')


def place_order(request):
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0

    cart_items = CartItem.objects.filter(user = request.user)
    
    if cart_items.count() < 1:
        return redirect('store')
    
    for item in cart_items:
        total += item.product.price * item.quantity
        
 
    
    tax = (2*total)/100 
    grand_total = total + tax
    
    if request.method == 'POST':
            order  = Order.objects.all()
        
            cart_items.save()
            return redirect('order_complete')
    return render(request, 'orders/place_order.html',{'cart_items' : cart_items, 'tax' : tax,'total' : total, 'grand_total' : grand_total})




def my_orders(request):
    orders = Order.objects.filter(user= request.user)
    context = {'orders': orders}
    return render(request, 'orders/my_orders.html', context)


def order_view(request, t_no):
    
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderItems = OrderProduct.objects.filter(order=order)
    context = {'order': order, 'orderItems': orderItems}

    return render(request, 'orders/order_view.html', context)
    

