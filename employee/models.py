import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from moduler.models import ModulerUserModel


# Create your models here.


class UserEmployee(models.Model):
    usermanager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employeemanager")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="employeeuser")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    to_moduler = models.IntegerField(null=True)
    android = models.BooleanField(default=False)
    wep = models.BooleanField(default=False)
    # moder = models.BooleanField(default=False)  # neeeeeeeeeewwww
    # bya3 = models.BooleanField(default=False)
    type_work = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"))
    email = models.EmailField(max_length=50, verbose_name=_("Email Address"))
    phone = models.CharField(max_length=50, null=True)
    rqmqume = models.CharField(max_length=14, default="")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=datetime.datetime.now())
    time_finshe = models.BooleanField(default=False)

    # events = models.DateTimeField()


    def __str__(self):
        return f"{self.full_name}"


class HadorEmployee(models.Model):
    usermanager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hadoremployeemanager")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    useremployee = models.ForeignKey(UserEmployee, on_delete=models.CASCADE, related_name="hadoremp")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    to_moduler = models.IntegerField(null=True)
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"))

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    hador = models.BooleanField(default=True)
    ansraf = models.BooleanField(default=False)

    # events = models.DateTimeField()


    def __str__(self):
        return f"{self.full_name}"
class Dof3atEmployee(models.Model):
    usermanager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dof3atemployeemanager")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    useremployee = models.ForeignKey(UserEmployee, on_delete=models.CASCADE, related_name="dof3atemp")
    moduler = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE)
    to_moduler = models.IntegerField(null=True)
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"))
    dof3a = models.DecimalField(decimal_places=2, max_digits=7, blank=False)
    start_time = models.DateTimeField(auto_now_add=True)