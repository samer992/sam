import datetime
from datetime import timezone
from time import strftime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

AUTH_PROVIDERS = {"email": "email", "google": "google", "facebook": "facebook"}


class User(AbstractBaseUser, PermissionsMixin):
    # user = models.ForeignKey(UserManager, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    email = models.EmailField(max_length=50, unique=True, verbose_name=_("Email Address"))

    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))
    # manager_user = models.ForeignKey(User, on_delete=models.CASCADE())#id manager
    manager = models.BooleanField(default=False)
    manageid = models.CharField(max_length=10)
    emp = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: ["first_name", "last_name"]
    objects = UserManager()
    def __str__(self):
        return self.email
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    profile_picture = models.ImageField(upload_to="profile_img/", default="profile_pictures/avatar_blank.jpg")
    logo_picture = models.ImageField(upload_to="logo_pictures/", default="profile_pictures/avatar_blank.jpg")
    shop_name = models.CharField(max_length=50, null=True)
    dec_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    post_code = models.CharField(max_length=6, null=True)


class UserManage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usermanage")
    # android = models.BooleanField(default=False)
    # wep = models.BooleanField(default=False)
    # desktop = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    events = models.DateTimeField()
    # manager = models.BooleanField(default=False)
    num_employee = models.IntegerField(default=1)
    # num_products = models.IntegerField(default=100)
    # emp = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.user}"




class Events(models.Model):
    title = models.CharField(max_length=50)
    dec = models.TextField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=7, blank=False)
    days = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

class FilesAdmin(models.Model):
    adminupload = models.FileField(upload_to="file-app/")
    title = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.title}"
