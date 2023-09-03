from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length= 100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField()
    status = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, default='')
    lname = models.CharField(max_length=150, default='')
    email = models.CharField(max_length=150, default='')
    phone = models.CharField(max_length=150, default='')
    address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=150, default='')
    state = models.CharField(max_length=150, default='')
    country = models.CharField(max_length=150, default='')
    order_total = models.FloatField()
    payment_mode = models.CharField(max_length=150, default='')
    orderstatuses = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default='Pending')
    # message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True, default='')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # price = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)
    
    
    