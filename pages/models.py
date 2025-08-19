from datetime import datetime
from accounts.models import User
from django.db import models
# import barcode

# Create your models here.

class HandelCartEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_pro_cart = models.IntegerField(default=0)
    num_emp_cart = models.IntegerField(default=0)
    event_id = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    android = models.BooleanField(default=False)
    wep = models.BooleanField(default=False)
    desktop = models.BooleanField(default=False)
