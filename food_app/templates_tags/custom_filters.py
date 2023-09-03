from django import template
import math

register = template.Library()

@register.filter
def apply_discount(price, discount_percentage):
    return math.ceil(price - (price * discount_percentage / 100))