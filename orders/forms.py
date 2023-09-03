from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['fname', 'lname', 'phone', 'email', 'address', 'city', 'state', 'country']
