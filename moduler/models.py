from django.db import models

from accounts.models import UserManage


# Create your models here.

class ModulerModel(models.Model):
    name = models.CharField(max_length=150, default="", blank=False)
    namee = models.CharField(max_length=150, default="", blank=False)
    namepath = models.CharField(max_length=150, default="", blank=False)
    imgmoduler = models.ImageField(upload_to="imgmoduler/", default="", blank=False)

    # is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ModulerUserModel(models.Model):
    name = models.CharField(max_length=150, default="", blank=False)
    namee = models.CharField(max_length=150, default="", blank=False)
    # namepath = models.CharField(max_length=150, default="", blank=False)
    imgmoduler = models.ImageField(upload_to="imgmoduler/", default="", blank=False)
    is_finished = models.BooleanField(default=False)
    usermanage = models.ForeignKey(UserManage, on_delete=models.CASCADE, related_name="mymodulers")
    num_products = models.IntegerField(default=200)
    clients = models.BooleanField(default=False)
    mandob = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class ProfileModuler(models.Model):
    modulerprofile = models.ForeignKey(ModulerUserModel, on_delete=models.CASCADE, related_name="modulerprof")
    profile_picture = models.ImageField(upload_to="profile_img/", default="profile_pictures/avatar_blank.jpg")
    logo_picture = models.ImageField(upload_to="logo_pictures/", default="profile_pictures/avatar_blank.jpg")
    shop_name = models.CharField(max_length=50, null=True)
    dec_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    post_code = models.CharField(max_length=6, null=True)
