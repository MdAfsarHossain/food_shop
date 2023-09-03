from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, related_name = 'account', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user.email)